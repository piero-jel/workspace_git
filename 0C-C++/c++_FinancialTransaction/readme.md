# Contenido
- [**Contenido**](#contenido)
- [**Financial Transaction**](#financial-transaction)
- [**Esquema de directorios de la Aplicacion**](#esquema-de-directorios-de-la-aplicacion)
- [**Verificacion Numero Tarjeta**](#verificacion-numero-tarjeta)
  + [**Archivo de Rangos**](#archivo-de-rangos)
  + [**Archivo de Etiquetas de Tarjetas**](#archivo-de-etiquetas-de-tarjetas)
  + [**Proceso de Verificación**](#proceso-de-verificación)
- [**Message**](#message)
  + [**Request Message**](#request-message)
  + [**Response Message**](#response-message)
  
- [**Compilacion**](#compilacion)
  + [Configuracion Makefile](#configuracion-makefile)
  
- [**Preparación del entorno**](#preparación-del-entorno)
  
- [**Server Host to Host**](#server-host-to-host)
- [**Run Examples**](#examples)
- [**unittests**](#unittests)
  
# Financial Transaction
 Financial Transaction se basa en un software que simule una transacción financiera. El mismo deberá solicitar un monto, numero de tarjeta y código de seguridad por teclado. Luego enviara un mensaje a un host que devolverá el estado de la transacción (aprobada o rechazada).
 
  1. Solicitar el monto de la compra con dos '2' decimales para los centavos.
  
  2. Solicitar el numero de tarjeta (longitud variable, mínimo 13 dígitos máximo 99).
  
  3. [**Verificar que el numero de tarjeta**](#verificacion-numero-tarjeta) corresponda a una tarjeta valida. Si no es valido mostrar el mensaje ***"TARJETA NO SOPORTADA"*** en pantalla y abortar la operación, de lo contrario mostrar el label de la tarjeta en pantalla y pasar al siguiente paso.
  
  4. Solicitar el código de seguridad (3-Dígitos).
  
  5. Armar el [**request message**](#request-message). Si transcurren mas de 5-Segundos o si ocurre otro error,  deberá mostrarse en pantalla ***"ERROR DE COMUNICACION"*** y abortar el proceso.
  
  6. Mostrar la respuesta en pantalla, en función del [**response message**](#response-message). Si el código de respuesta es **"00"** , indica que la transacción fue aprobada y deberá mostrar ***"APROBADA"*** en pantalla. Si el codigo de respuesta es cualquier otro valor, deberá mostrar ***"RECHAZADA"*** .
 
# Esquema de directorios de la Aplicacion

<details><summary><b>Tree Directory</b></summary>

``` bash
.
├── app     # Directorios de los ejecutables
├── files   # Directorios con los archivos para validación de tarjetas
│   └── local
│       ├── cards.dat
│       ├── ranges.dat
│       └── test.dat
├── inc     # Directorio con los header files del proyecto
│   ├── CardsRegister.hpp
│   ├── financial_transaction.hpp
│   ├── main.hpp
│   ├── PSocket.hpp
│   └── RangesRegister.hpp
├── Makefile   # Archivo con los target para compilar y ejecutar
├── out        # Directorio intermedio para la compilación
├── readme.md  # este archivo
└── src        # Directorio con los archivos fuentes
    ├── CardsRegister.cpp
    ├── financial_transaction.cpp
    ├── main.cpp
    ├── PSocket.cpp
    ├── RangesRegister.cpp
    ├── server.cpp
    └── unittests.cpp

```

</details><br>

  + **app** : Directorio donde se colocaran los ejecutables.
    - **FinancialTransaction_v0** : de la aplicación.
    - **Host2HostServer** : el server o emulación del servicio.
    - **unittest_app** : ejecutable con los unittests

  + **files** : Directorio que contiene archivos, dentro de este tenenos el subdirectorio local con los archivos de rango y tarjetas asociados a la ejecución del proyecto.
  
  + **inc** : Directorio donde se localizan los header files.
  + **src** : Directorio donde colocamos los source files.
  + **Makefile** : Archivo con los target de compilación para **`make`**.
  + **out** : Directorio donde se colocaran los object files, resultado de la compilación.
  + **readme.md** : este documento .
  
  
Debemos considerar que dentro de los **sources files** tenemos tres archivos importantes:

  - **`src/main.cpp`** archivo principal con el core del proyecto.
  - **`src/server.cpp`** código para emular el servicio al cual reporta el proyecto. 
  - **`src/unittests.cpp`** los test cases del unit tests.
  
  > Todos ellos con su correspondiente función `main()`, por lo que se aconseja manejar/editar con cuidado el archivo **`Makefile`**, ya que se pueden modificar los filter y se intente compilar combinaciones de estos. Lo que arrojara errores relacionados al comando **`make`**.
  
  
  
# Verificacion Numero Tarjeta
La verificación del numero de tarjeta se basa en el uso de dos archivos uno de rangos y el otro con las etiquetas de cada tarjeta (**`Ranges.dat`**, **`Cards.dat`**). Cada uno de estos posee un formato de registros por cada linea que lo compone.

  - [**Archivo de Rangos**](#archivo-de-rangos)
  - [**Archivo de Etiquetas de Tarjetas**](#archivo-de-etiquetas-de-tarjetas)
  - [**Proceso de Verificación**](#proceso-de-verificacion)
  
## Archivo de Rangos
``` bash
# RANGE_LOW(8)~RANGE_HIGHT(8)~LEN(2BYTES)~ID(4BYTES)
45176501 45176600 16 0010
```
  - **RANGE_LOW** : low value del rango, 8 dígitos.
  - **RANGE_HIGHT** : hight value del rango, 8 dígitos.
  - **LEN** : longitud del numero de tarjeta, 2 dígitos.
  - **ID** : identificador único de Tarjeta, 4 dígitos
  
Tenemos un carácter de separación entre cada item, este puede ser cualquier incluso un espacio en blanco, por lo general se usa el símbolo **'~'**.
  
  
## Archivo de Etiquetas de Tarjetas
``` bash
# LABEL(12)~ID(4BYTES)
BNC Nro111-1 0100
```
  - **LABEL** : Etiqueta de la entidad financiera a la cual pertenece la tarjeta, 12 dígitos
  - **ID** : identificador único de Tarjeta, 4 dígitos.
  

  
## Proceso de Verificación
Dado un numero de tarjeta, se leerán todos los registros del [**archivo de rangos**](#archivo-de-rangos) y se compararan los primeros 8 dígitos del numero de tarjeta con cada registro. Básicamente que estos 8 dígitos que forman un valor estén comprendido entre el rango de alguno de los registros (el valor puede ser igual a los limites).


Si el valor de los primero 8 dígitos esta comprendido por alguno de los registros, se toma de este la longitud y el id. De lo contrario se cancela la operación.

Con la longitud del registro comparamos la longitud del numero de tarjeta aportado, si estos no coinciden se cancela la operación ya que se considera un numero de tarjeta incorrecto.

En este punto tenemos el ID de tarjeta, tomado del registro desde el archivo de rangos, con este podemos buscar los datos dentro del [**Archivo de etiquetas de tarjetas**](#archivo-de-etiquetas-de-tarjetas) y así obtenemos el label de la misma para proceder con la operación.


# Message
  - [**Request Message**](#request-message)
  - [**Response Message**](#response-message)
  
## Request Message
Formato del mensaje request para el servidor, todos los campos para este caso deben ser ASCII.

``` 
Request:
 -------------------------------------
|  MTID  | Nro Tarjeta | Monto | Code |
 -------------------------------------
```

  + **MTID** : Message Type Identificator, longitud fija hasta 4 dígitos. Para el Request este debe ser **0200**.
  
  + **Nro Tarjeta** : la longitud de este es variable ( 13 ~ 99 dígitos), por lo que los dos dígitos del inicio indicaran la longitud del numero de tarjeta y lo sigue el numero de la misma.
  
  + **Monto** : Este tiene una longitud fija de hasta 12 dígitos sin separador decimal (dos decimales implícitos) y con relleno de '0' del lado izquierdo.
  
  + **Code** : Código de Seguridad, con longitud fija de 3 dígitos.


Ejemplo:
  - **Nro Tarjeta** : 4517650654628311
  - **Monto** ($124,54): 124.54 
  - **Code** : 123

  
<!--
``` 
Request:
 -------------------------------------------------
| MTID |    Nro Tarjeta     |     Monto    | Code | 
 -------------------------------------------------
| 0200 | 164517650654628311 | 000000012454 | 123  |
 -------------------------------------------------
```
-->
 


| **MTID** | **Nro Tarjeta**    | **Monto**    | **Code** | 
|:--------:|:------------------:|:------------:|:--------:|
|   0200   | 164517650654628311 | 000000012454 | 123      |
|          |                    |              |          | 

  
## Response Message
Formato del mensaje Response devuelto por el servidor, todos los campos para este caso deben ser **ASCII**.

``` 
Request:
 -------------------
|  MTID  | RespCode |
 -------------------
```

  + **MTID** : Message Type Identificator, longitud fija hasta 4 dígitos. Para el Response este debe ser **0210**.
  
  + **RespCode** : El codigo de respuesta la longitud de este es fija de dos dígitos, código igual a **`00`** significa transacción aprobada. Mientras que un valor distinto a este, para este caso, significa transacción rechazada.
    

Ejemplos:
  - Code : **`00`**, succes
  - Code : **`47`**, no succes
  
| **MTID**   | **RespCode** | **Status**  |
|:----------:|:------------:|:------------|
| **`0210`** | **`  00`**   | **SUCCESS** |
| **`0210`** | **`!=00`**   | **FAILURE** |
 


<!-- 
``` 
Request:
 -----------------
| MTID | RespCode |
 -----------------
| 0210 |    00    | SUCCESS
 -----------------  
| 0210 |    47    | FAILURE
 -----------------
~~
-->
 
# Compilacion
Dentro del directorio root tenemos un **Makefile** con los siguientes targets:

  + **`make all`** : default, este compila los sources.
  + **`make clean`** : elimina los objects files y el ejecutable.
  + **`make new`** : ejecuta un clean y vuelve a compilar.
  + **`make run`** : Si no se compilo aun compila los sources y luego ejecuta.
  + **`make debug`** : Este lanza una sesión de gdb para el debug del proyecto.
  + **`make server`** : Compila solo el codigo correspondiente al server.
  + **`make unittests`** : Compila solo el codigo correspondiente a los unit tests.
  
  
Para que los target anteriores pueda ejecutarse se recomienda tener instalado **gcc/g++**, y **make**, de caso contrario debemos instalarlos.

Los target **run** y **debug** tiene habilitado la variable ARGS con la cual le pasamos al ejecutable (o session de **GDB**) los argumentos.
  
## Configuracion Makefile
La configuración Básica contempla:
  
  + Selección de la versión del estándar de compilación **`STD_VER`** por defecto esta en '2023', que representa el estándar de **`-std=c++23`** (en su defecto para **GNU** **`-std=gnu++23`**).
  
  + Setting de depuración de memoria **`DEBUG_ON`**, por defecto '0':
    - 0 : Deshabilita las opciones de debug.
    - 1 : Habilita el **sanitize** para el tracking de memoria reservada (monitoreo del Heap) en tiempo de ejecución.
    - 2 : Habilita solo los Flags de GDB (para **`make debug`** este se establece de forma automática).
    
> **Para el unittest se recomienda el estandar STD_VER con valores 2020, 2023 o superiores**.



# Preparación del entorno
Este depende de que distribución estemos usando, para estos ejemplos tenemos :

<details><summary style="font-weight: bold; font-size: 14px;"><b>Instalación Fedora Red Hat</b></summary>

``` bash
sudo dnf update -y
sudo dnf install -y gcc gdb make libasan libubsan gcc gcc-c++
```

</details>
<details><summary style="font-weight: bold; font-size: 14px;"><b>Instalación Debian</b></summary>

``` bash
## apt get
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install -y build-essential make gdb

## aptitude
sudo apt update && sudo apt upgrade -y
sudo apt install -y build-essential make gdb
```

</details>
<br>



# Server Host to Host
Para emular el servidor contamos con el source **`server.cpp`** que contiene el código del server, con el cual podemos lanzar pruebas. Para compilar y ejecutar este solo debemos ejecutar los siguentes target de **`Makefile`**:

<details><summary><b>make server</b></summary>

``` bash
# solo compila
make server

# compila y lanza el server
make server_run
```

</details>
<details><summary><b>run server</b></summary>

``` bash
==========[ BEGIN, compiling C++ file ./src/server.cpp ]==========
==========[ END, compiling C++ file ./src/server.cpp ]==========


===========[BEGIN, compiling VERSION: 0, STD_VER: 2020 ]==========

Tamaño del archivo ejecutable formato:
   text    data     bss     dec     hex filename
  61428    1388     320   63136    f6a0 ./app/Host2HostServer
===========[END, compiling: "Host2HostServer"]==========

Server Up in <0.0.0.0:3000>
```
    
</details>

  > Para finalizar o salir de la aplicacion solo debemos ingresar la secuencia **`Ctrl+c`**.

Este visualiza la direccion **IP** y el puerto en el que se encuentra escuchando peticiones. En caso de necesitar realizar cambios solo debemos ejecutar nuevamente el target, o en su defecto un clean pervio:

``` bash
make clean
make server

# o directamente compilando y ejecutando
make clean
make server_run
```

En caso de querer ejecutarlo directamente el binario solo debemos realizarlo de la siguente manera:

```bash
app/Host2HostServer_v1 3000
```

<details><summary><b>example run</b></summary>

``` bash
Server Up in <0.0.0.0:3000>

# cuando el cliente se conecte
Connected to Client <127.0.0.1:33955>

# cuando el cliente envié el mensaje
Msg Arrivado <0200164517650654628311000000012454123>

# En este paso nos pedirá ingresar el código de respuesta
Ingrese Codigo de Respuesta: 00
```
    
</details>


# Examples

<details><summary><b>make all</b></summary>

``` bash
make 

===========[BEGIN, compiling VERSION: 0, STD_VER: 2020 ]==========

Tamaño del archivo ejecutable formato:
   text    data     bss     dec     hex filename
  79329    1808     640   81777   13f71 ./app/FinancialTransaction_v0
===========[END, compiling: "FinancialTransaction_v0"]==========

```

</details>
<details><summary><b>make new</b></summary>

``` bash
make new

===========[ clean files ... ]==========

===========[BEGIN, compiling VERSION: 0, STD_VER: 2020 ]==========

Tamaño del archivo ejecutable formato:
   text    data     bss     dec     hex filename
  79329    1808     640   81777   13f71 ./app/FinancialTransaction_v0
===========[END, compiling: "FinancialTransaction_v0"]==========
```

</details>
<br>

<div style="display: grid; grid-template-columns: 1fr 1fr;">
<div style="text-align: left; font-size: 14px">

**Datos para Testing**
1. Ingresar el saldo, solo hasta dos dígitos decimales (dos dígitos después del punto decimal), *ex ($124,54): 124.54* 

2. Ingreso NroTarjeta, *ex: 4517650654628311*

3. Ingreso de Clave de seguridad (solo 3-Digito), *ex: 123*

Esto debe enviar al server el msg con el **MTID 0200** y demás datos.
  
4. Del lado del servidor se recibirá la respuesta con el **MTID 0210** seguida del código:
  - '00' , aprobada ok
  - Distinto de '00' error, trx rechazada.

<!-- 
Ingrese el monto (hasta 2 decimales Implícitos): 124.54
Ingrese el Numero de Tarjeta ( 13 ~ 99 decimales): 4517650654628311
Ingrese el Código de Seguridad (hasta 3 dígitos): 123
El Saldo ingresado es: 12454
El Numero de tarjeta ingresado es: 4517650654628311
El Código de tarjeta ingresado es: 123
Request to send: 0200164517650654628311000000012454123

| 0200 | 16 4517650654628311 | 000000012454 | 123

-->

    
</div>
<div style="text-align: left; font-size: 14px">
<details><summary><b>run server</b></summary>

Sobre una terminal ejecutamos el server, de la siguente forma:

```bash
make server_run 

==========[ BEGIN, compiling C++ file ./src/CardsRegister.cpp ]==========
==========[ END, compiling C++ file ./src/CardsRegister.cpp ]==========


==========[ BEGIN, compiling C++ file ./src/financial_transaction.cpp ]==========
==========[ END, compiling C++ file ./src/financial_transaction.cpp ]==========


==========[ BEGIN, compiling C++ file ./src/PSocket.cpp ]==========
==========[ END, compiling C++ file ./src/PSocket.cpp ]==========


==========[ BEGIN, compiling C++ file ./src/RangesRegister.cpp ]==========
==========[ END, compiling C++ file ./src/RangesRegister.cpp ]==========


==========[ BEGIN, compiling C++ file ./src/server.cpp ]==========
==========[ END, compiling C++ file ./src/server.cpp ]==========


===========[BEGIN, compiling VERSION: 0, STD_VER: 2020 ]==========

Tamaño del archivo ejecutable formato:
   text    data     bss     dec     hex filename
  61689    1516     320   63525    f825 ./app/Host2HostServer
===========[END, compiling: "Host2HostServer"]==========

Server Up in <0.0.0.0:3000>


```
  > Para detener este, en caso de no ejecutar el cliente, debemos presionar la combinacion **`Ctrl+c`**.
  
</details>
<details><summary><b>run client</b></summary>

Sobre una nueva terminal ejecutamos el clien:

``` bash
make clean
make run

===========[BEGIN, compiling VERSION: 0, STD_VER: 2020 ]==========

Tamaño del archivo ejecutable formato:
   text    data     bss     dec     hex filename
  79329    1808     640   81777   13f71 ./app/FinancialTransaction_v0
===========[END, compiling: "FinancialTransaction_v0"]==========

./app/FinancialTransaction_v0 ARGS = '-r files/local/ranges.dat -c files/local/cards.dat', CASE = ''
-i <ip>      : 0.0.0.0
-p <port>    : 3000
-t <timeout> : 5000 [mSec]
-c <path/card-file>: files/local/cards.dat
-r <path/range-file>: files/local/ranges.dat
Client Connect to <0.0.0.0:3000>
Ingrese el monto (hasta 2 decimales Implicitos): 124.54
Ingrese el Numero de Tarjeta ( 13 ~ 99 decimales): 4517650654628311
TARJETA <4517650654628311>, CARD LABEL <BAN Nro 0010>
Ingrese el Codigo de Seguridad (hasta 3 digitos): 123
El Saldo ingresado es: 12454
El Numero de tarjeta ingresado es: 4517650654628311
El Codigo de tarjeta ingresado es: 123
Request to send: 0200164517650654628311000000012454123
Response: 021000
OPERACION APROVADA
```

  > Para este caso debemos considerar que tenemos un server escuchando en la ip y puerto cargado como parámetro **ARGS**.

</details>
</div>
</div>
<br>

<div style="display: grid; grid-template-columns: 1fr 1fr;">
<div style="text-align: left; font-size: 14px">

<details><summary><b>run executable sin server</b></summary>

``` bash
app/FinancialTransaction_v0 -i 127.0.0.1 -p3000 -t10000 -r files/local/ranges.dat -c files/local/cards.dat
-i <ip>      : 127.0.0.1
-p <port>    : 3000
-t <timeout> : 10000 [mSec]
-c <path/card-file>: files/local/cards.dat
-r <path/range-file>: files/local/ranges.dat
Error "Could not bind to Server <127.0.0.1:3000>"
```
  > ***Para este caso vemos la respuesta cuando el servidor no esta disponible o los datos aportados no son correctos***.

</details>
    
</div>
<div style="text-align: left; font-size: 14px">
    
<details><summary><b>run executable with server up</b></summary>

``` bash
app/FinancialTransaction_v0 -i 127.0.0.1 -p3000 -t10000 -r files/local/ranges.dat -c files/local/cards.dat
-i <ip>      : 127.0.0.1
-p <port>    : 3000
-t <timeout> : 10000 [mSec]
-c <path/card-file>: files/local/cards.dat
-r <path/range-file>: files/local/ranges.dat
Client Connect to <127.0.0.1:3000>
Ingrese el monto (hasta 2 decimales Implicitos): 254,879
Ingrese el Numero de Tarjeta ( 13 ~ 99 decimales): 4517650654628311
TARJETA <4517650654628311>, CARD LABEL <BAN Nro 0010>
Ingrese el Codigo de Seguridad (hasta 3 digitos): 321
El Saldo ingresado es: 25400
El Numero de tarjeta ingresado es: 4517650654628311
El Codigo de tarjeta ingresado es: 321
Request to send: 0200164517650654628311000000025400321
Response: 021089
OPERACION RECHAZADA CON EL CODIGO <89>
```

</details>
</div>
</div>
<br>




# unittests

<div style="display: grid; grid-template-columns: 1fr 1fr;">
<div style="text-align: left; font-size: 14px">

Compilación de los unittests

<details><summary><b>make unittests</b></summary>

```bash
make unittests
```
</details>
<details><summary><b>compile</b></summary>

```bash
make clean
make unittests

==========[ BEGIN, compiling C++ file ./src/CardsRegister.cpp ]==========
==========[ END, compiling C++ file ./src/CardsRegister.cpp ]==========


==========[ BEGIN, compiling C++ file ./src/financial_transaction.cpp ]==========
==========[ END, compiling C++ file ./src/financial_transaction.cpp ]==========


==========[ BEGIN, compiling C++ file ./src/PSocket.cpp ]==========
==========[ END, compiling C++ file ./src/PSocket.cpp ]==========


==========[ BEGIN, compiling C++ file ./src/RangesRegister.cpp ]==========
==========[ END, compiling C++ file ./src/RangesRegister.cpp ]==========


==========[ BEGIN, compiling C++ file ./src/unittests.cpp ]==========
==========[ END, compiling C++ file ./src/unittests.cpp ]==========


===========[BEGIN, compiling VERSION: 0, STD_VER: 2020 ]==========

Tamaño del archivo ejecutable formato:
   text    data     bss     dec     hex filename
 191779    1700     368  193847   2f537 ./app/unittest_app
===========[END, compiling: "unittest_app"]==========
```
    
</details>
</div>
<div style="text-align: left; font-size: 14px">

Ejecución de los unittests

<details><summary><b>make unittests_run</b></summary>

```bash
make unittests_run

===========[BEGIN, compiling VERSION: 0, STD_VER: 2020 ]==========

Tamaño del archivo ejecutable formato:
   text    data     bss     dec     hex filename
 191749    1700     368  193817   2f519 ./app/unittest_app
===========[END, compiling: "unittest_app"]==========


Test ExecuteTestCases, current pointer
Inicio de la ejecucion Class TestPSocket
response: test    0
response: test    1
response: test    2
response: test    3
response: test    4
client.Disconnect() err :0
Run Sucess Method echo
close() err :0
Fin    de la ejecucion Class TestPSocket

Inicio de la ejecucion Class TestAmount
Run Sucess Method get_ok
Run Sucess Method get_ok_list
Run Sucess Method get_not_number
Run Sucess Method get_too_long
Run Sucess Method get_neg_value
Fin    de la ejecucion Class TestAmount

Inicio de la ejecucion Class TestCardCode
Run Sucess Method get_ok
Run Sucess Method get_ok_list
Run Sucess Method get_not_number
Run Sucess Method get_too_long
Fin    de la ejecucion Class TestCardCode

Inicio de la ejecucion Class TestCardNumber
Run Sucess Method get_ok
Run Sucess Method get_ok_list
Run Sucess Method get_too_short
Run Sucess Method get_not_number
Fin    de la ejecucion Class TestCardNumber

Inicio de la ejecucion Class TestVerifyCardNumber
Card Register  : <BAN Nro 0010> | <10>
Range Register : <[45176501] [45176600]> | <16> | <10>
Run Sucess Method get_ok
Run Sucess Method get_nok
Run Sucess Method frange_notfound
Run Sucess Method fcards_notfound
Fin    de la ejecucion Class TestVerifyCardNumber

Run 18 test case, 18 Success and 0 with error.

```

</details>
</div>
</div>

  > No es necesario ejecutar en secuencia, primero el `make unittests` y luego `make unittests_run` si solo queremos ejecutar los mismos. Al estar armada las dependencias dentro del makefile con solo ejecutar `make unittests_run` se compilara lo necesario para armar el binario correspondiente para luego ejecutarlo.







