# Contenido
  + [Financial Transaction, Descripción del Proyecto](#financial-transaction)
  
  + [Verificación Numero Tarjeta](#verificacion-numero-tarjeta)
    - [Archivo de Rangos](#archivo-de-rangos)
    - [Archivo de Etiquetas de Tarjetas](#archivo-de-etiquetas-de-tarjetas)
    - [Proceso de Verificación](#proceso-de-verificacion)
    
  + [Message](#message)
    - [Request Message](#request-message)
    - [Response Message](#response-message)
  
  + [Compilación](#compilacion)
    - [Instalación Red Hat](#instalaccion-red-hat)
    - [Instalación Debian](#instalaccion-debian)
    - [Configuración Makefile](#configuracion-makefile)
  
  + [Server Host to Host](#server-host-to-host)
  
  + [Examples](#examples)
    - [make all](#make-all)
    - [make new](#make-new)
    - [Datos para Testing](#datos-para-testing)
    - [make run](#make-run)
    - [run executable](#run-executable)

# Financial Transaction
 Financial Transaction se basa en un software que simule una transacción financiera. El mismo debera solicitar un monto, numero de tarjeta y código de seguridad por teclado. Luego enviara un mensaje a un host que devolverá el estado de la transacción (aprobada o rechazada).
 
  1. Solicitar el monto de la compra con dos '2' decimales para los centavos.
  
  2. Solicitar el numero de tarjeta (longitud variable, mínimo 13 dígitos máximo 99).
  
  3. [Verificar que el numero de tarjeta](#verificacion-numero-tarjeta) corresponda a una tarjeta valida. Si no es valido mostrar el mensaje ***"TARJETA NO SOPORTADA"*** en pantalla y abortar la operación, de lo contrario mostrar el label de la tarjeta en pantalla y pasar al siguiente paso.
  
  4. Solicitar el código de seguridad (3-Digitos).
  
  5. Armar el [request message](#request-message). Si transcurren mas de 5-Segundos o si ocurre otro error,  deberá mostrarse en pantalla ***"ERROR DE COMUNICACION"*** y abortar el proceso.
  
  6. Mostrar la respuesta en pantalla, en función del [response message](#response-message). Si el código de respuesta es **"00"** , indica que la transacción fue aprobada y deberá mostrar ***"APROBADA"*** en pantalla. Si el codigo de respuesta es cualquier otro valor, deberá mostrar ***"RECHAZADA"*** .
 
# Verificacion Numero Tarjeta
La verificación del numero de tarjeta se basa en el uso de dos archivos uno de rangos y el otro con las etiquetas de cada tarjeta (```Ranges.dat```, ```Cards.dat```). Cada uno de estos posee un formado de registros por cada linea que lo compone.

  - [Archivo de Rangos](#archivo-de-rangos)
  - [Archivo de Etiquetas de Tarjetas](#archivo-de-etiquetas-de-tarjetas)
  - [Proceso de Verificación](#proceso-de-verificacion)
  
## Archivo de Rangos
~~~ bash
# RANGE_LOW(8)~RANGE_HIGHT(8)~LEN(2BYTES)~ID(4BYTES)
45176501 45176600 16 0010
~~~
  - RANGE_LOW : low value del rango, 8 dígitos.
  - RANGE_HIGHT : hight value del rango, 8 dígitos.
  - LEN : longitud del numero de tarjeta, 2 dígitos.
  - ID : identificador único de Tarjeta, 4 dígitos
  
Tenemos un carácter de separación entre cada item, este puede ser cualquier incluso un espacio en blanco, por lo general se usa el símbolo '~'
  
  
## Archivo de Etiquetas de Tarjetas
~~~ bash
# LABEL(12)~ID(4BYTES)
BNC Nro111-1 0100
~~~
  - **LABEL** : Etiqueta de la entidad financiera a la cual pertenece la tarjeta, 12 dígitos
  - **ID** : identificador único de Tarjeta, 4 dígitos.
  

  
## Proceso de Verificacion
Dado un numero de tarjeta, se leerán todos los registros del [archivo de rangos](#archivo-de-rangos) y se compararan los primeros 8 dígitos del numero de tarjeta con cada registro. Básicamente que estos 8 dígitos que forman un valor estén comprendido entre el rango de alguno de los registros (el valor puede ser igual a los limites).


Si el valor de los primero 8 dígitos esta comprendido por alguno de los registros, se toma de este la longitud y el id. De lo contrario se cancela la operación.

Con la longitud del registro comparamos la longitud del numero de tarjeta aportado, si estos no coinciden se cancela la operación ya que se considera un numero de tarjeta incorrecto.

En este punto tenemos el ID de tarjeta, tomado del registro desde el archivo de rangos, con este podemos buscar los datos dentro del [Archivo de etiquetas de tarjetas](#archivo-de-etiquetas-de-tarjetas) y así obtenemos el label de la misma para proceder con la operación.


  



# Message
  - [Request Message](#request-message)
  - [Response Message](#response-message)
  
## Request Message
Formato del mensaje request para el servidor, todos los campos para este caso deben ser ASCII.

~~~ 
Request:
 -------------------------------------
|  MTID  | Nro Tarjeta | Monto | Code |
 -------------------------------------
~~~

  + **MTID** : Message Type Identificator, longitud fija hasta 4 dígitos. Para el Request este debe ser **0200**.
  
  + **Nro Tarjeta** : la longitud de este es variable ( 13 ~ 99 dígitos), por lo que los dos dígitos del inicio indicaran la longitud del numero de tarjeta y lo sigue el numero de la misma.
  
  + **Monto** : Este tiene una longitud fija de hasta 12 dígitos sin separador decimal (dos decimales implícitos) y con relleno de '0' del lado izquierdo.
  
  + **Code** : Código de Seguridad, con longitud fija de 3 dígitos.


Ejemplo:
  - Nro Tarjeta : 4517650654628311
  - Monto ($124,54): 124.54 
  - Code : 123
  
~~~ 
Request:
 -------------------------------------------------
| MTID |    Nro Tarjeta     |     Monto    | Code | 
 -------------------------------------------------
| 0200 | 164517650654628311 | 000000012454 | 123  |
 -------------------------------------------------
~~~
  
## Response Message
Formato del mensaje Response devuelto por el servidor, todos los campos para este caso deben ser ASCII.

~~~ 
Request:
 -------------------
|  MTID  | RespCode |
 -------------------
~~~

  + **MTID** : Message Type Identificator, longitud fija hasta 4 dígitos. Para el Response este debe ser **0210**.
  
  + **RespCode** : El codigo de respuesta la longitud de este es fija de dos dígitos, código igual a ```00``` significa transacción aprobada. Mientras que un valor distinto a este, para este caso, significa transacción rechazada.
    

Ejemplos:
  - Code : 00, succes
  - Code : 47, no succes
  
~~~ 
Request:
 -----------------
| MTID | RespCode |
 -----------------
| 0210 |    00    | SUCCESS
 -----------------  
| 0210 |    47    | FAILURE
 -----------------
~~~
 
# Compilacion
Dentro del directorio root tenemos un **Makefile** con los siguientes targets:

  + ```make all``` : default, este compila los sources.
  + ```make clean``` : elimina los objects files y el ejecutable.
  + ```make new``` : ejecuta un clean y vuelve a compilar.
  + ```make run``` : Si no se compilo aun compila los sources y luego ejecuta.
  + ```make debug``` : Este lanza una sesión de gdb para el debug del proyecto.
  
Para que los target anteriores pueda ejecutarse se recomienda tener instalado **gcc/g++**, y **make**, de caso contrario debemos instalarlos.

Los target **run** y **debug** tiene habilitado la variable ARGS con la cual le pasamos al ejecutable (o session de GDB) los argumentos.


## Instalaccion Red Hat
~~~ bash
  yum update
  yum install -y gcc gdb make llvm-toolset yum-utils libasan
~~~

## Instalaccion Debian
~~~ bash
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install -y build-essential gdb
~~~



  
  
## Configuracion Makefile
La configuración Básica contempla:
  1. Selección de la versión del proyecto ```VERSION```, por defecto '0' tenemos una sola versión para este caso.
  2. Selección de la versión del estándar de compilación ```STD_VER``` por defecto esta en '2020', que representa el estándar de c++20.
  3. Setting de depuración de memoria ```DEBUG_ON```, por defecto '0'.
    - 0 : Deshabilita las opciones de debug.
    - 1 : Habilita el **sanitize** para el tracking de memoria reservada (monitoreo del Heap) en tiempo de ejecución.
    - 2 : Habilita solo los Flags de GDB (para ```make debug``` este se establece de forma automática).
    

# Server Host to Host
La versión 1 del source ```main.cpp``` contiene el código del server, con el cual podemos lanzar pruebas. Para compilar este solo debemos colocar el valor de ```VERSION``` en uno. Otra opción es compilarlo con el valor de versión en la acción:

~~~ bash
make VERSION=1

===========[BEGIN, compiling VERSION: 1, STD_VER: 2020 ]==========

Tamaño del archivo ejecutable formato:
   text    data     bss     dec     hex filename
  42146    1640     640   44426    ad8a ./app/Host2HostServer_v1
===========[END, compiling: "Host2HostServer_v1"]==========
~~~
En caso de realizar cambios podemos ejecutar el target **new** de la siguiente manera:

~~~ bash
make new VERSION=1

===========[ clean files ... ]==========

===========[BEGIN, compiling VERSION: 1, STD_VER: 2020 ]==========

Tamaño del archivo ejecutable formato:
   text	   data	    bss	    dec	    hex	filename
  40297	   1544	    640	  42481	   a5f1	./app/Host2HostServer_v1
===========[END, compiling: "Host2HostServer_v1"]==========

~~~
De la misma forma los demás target ( debug o ```make debug VERSION=1```) están disponible para admitir el valor de la versión.

Con el código ya compilado ejecutamos el mismo:

~~~ bash
app/Host2HostServer_v1 3000
Server Up in <0.0.0.0:3000>

# cuando el cliente se conecte
Connected to Client <127.0.0.1:33955>

# cuando el cliente envié el mensaje
Msg Arrivado <0200164517650654628311000000012454123>

# En este paso nos pedirá ingresar el código de respuesta
Ingrese Codigo de Respuesta: 00
~~~

# Examples
  - [make all](#make-all)
  - [make new](#make-new)
  - [Datos para Testing](#datos-para-testing)
  - [make run](#make-run)
  - [run executable](#run-executable)
    
## make all
~~~ bash
make 

===========[BEGIN, compiling VERSION: 0, STD_VER: 2020 ]==========

Tamaño del archivo ejecutable formato:
   text    data     bss     dec     hex filename
  79329    1808     640   81777   13f71 ./app/FinancialTransaction_v0
===========[END, compiling: "FinancialTransaction_v0"]==========

~~~

## make new
~~~ bash
make new

===========[ clean files ... ]==========

===========[BEGIN, compiling VERSION: 0, STD_VER: 2020 ]==========

Tamaño del archivo ejecutable formato:
   text    data     bss     dec     hex filename
  79329    1808     640   81777   13f71 ./app/FinancialTransaction_v0
===========[END, compiling: "FinancialTransaction_v0"]==========
~~~

## Datos para Testing
  1. Ingresar el saldo, solo hasta dos dígitos decimales (dos dígitos después del punto decimal), *ex ($124,54): 124.54* 

  2. Ingreso NroTarjeta, *ex: 4517650654628311*

  3. Ingreso de Clave de seguridad (solo 3-Digito), *ex: 123*
  
Esto debe enviar al server el msg con el MTID 0200 y demás datos.
    
  4. Del lado del servidor se recibirá la respuesta con el MTID 0210 seguida del código
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

## make run
~~~ bash
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
~~~
Para este caso debemos considerar que tenemos un server escuchando en la ip y puerto cargado como parámetro **ARGS**.

## run executable
~~~ bash
app/FinancialTransaction_v0 -i 127.0.0.1 -p3000 -t10000 -r files/local/ranges.dat -c files/local/cards.dat
-i <ip>      : 127.0.0.1
-p <port>    : 3000
-t <timeout> : 10000 [mSec]
-c <path/card-file>: files/local/cards.dat
-r <path/range-file>: files/local/ranges.dat
Error "Could not bind to Server <127.0.0.1:3000>"
~~~
Para este caso vemos la respuesta cuando el servidor no esta disponible o los datos aportados no son correctos.

~~~ bash
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
~~~








