# Contenido
  + [Financial Transaction, Descripción del Proyecto](#financial-transaction)
  
  + [Verificación Numero Tarjeta](#verificacion-numero-tarjeta)
    - [Archivo de Rangos](#archivo-de-rangos)
    - [Archivo de Etiquetas de Tarjetas](#archivo-de-etiquetas-de-tarjetas)
    - [Proceso de Verificación](#proceso-de-verificacion)
    
  + [Message](#message)
    - [Request Message](#request-message)
    - [Response Message](#response-message)
    
  + [Instalaccion python](#instalaccion-python)
    - [Instacion python linux](#instacion-python-linux)
    - [Instacion pip linux](#instacion-pip-linux)
    - [Instalación dependencias del proyecto](#instalaccion-dependencias-del-proyecto)
  
  + [Esquema de directorios de la Aplicación](#esquema-de-directorios-de-la-aplicacion)
  
  + [Ejecución del proyecto](#ejecucion-del-proyecto)
    - [Ejecución del server](#ejecuccion-del-server)
    - [Ejecución Cliente](#ejecuccion-cliente)
    - [Side Client Server down](#side-client-server-down)
    - [Side Client Server timeout](#side-client-server-timeout)


# Financial Transaction
 Financial Transaction se basa en un software que simule una transacción financiera. El mismo deberá solicitar un monto, numero de tarjeta y código de seguridad por teclado. Luego enviara un mensaje a un host que devolverá el estado de la transacción (aprobada o rechazada).
 
  1. Solicitar el monto de la compra con dos '2' decimales para los centavos.
  
  2. Solicitar el numero de tarjeta (longitud variable, mínimo 13 dígitos máximo 99).
  
  3. [Verificar que el numero de tarjeta](#verificacion-numero-tarjeta) corresponda a una tarjeta valida. Si no es valido mostrar el mensaje ***"TARJETA NO SOPORTADA"*** en pantalla y abortar la operación, de lo contrario mostrar el label de la tarjeta en pantalla y pasar al siguiente paso.
  
  4. Solicitar el código de seguridad (3-Digitos).
  
  5. Armar el [request message](#request-message). Si transcurren mas de 5-Segundos o si ocurre otro error,  deberá mostrarse en pantalla ***"ERROR DE COMUNICACION"*** y abortar el proceso.
  
  6. Mostrar la respuesta en pantalla, en función del [response message](#response-message). Si el código de respuesta es **"00"** , indica que la transacción fue aprobada y deberá mostrar ***"APROBADA"*** en pantalla. Si el código de respuesta es cualquier otro valor, deberá mostrar ***"RECHAZADA"*** .
 
# Verificacion Numero Tarjeta
La verificación del numero de tarjeta se basa en el uso de dos archivos uno de rangos y el otro con las etiquetas de cada tarjeta (```Ranges.dat```, ```Cards.dat```). Cada uno de estos posee un formato de registros por cada linea que lo compone.

  - [Archivo de Rangos](#archivo-de-rangos)
  - [Archivo de Etiquetas de Tarjetas](#archivo-de-etiquetas-de-tarjetas)
  - [Proceso de Verificación](#proceso-de-verificacion)
  
## Archivo de Rangos
~~~ bash
# RANGE_LOW(8)~RANGE_HIGHT(8)~LEN(2BYTES)~ID(4BYTES)
45176501 45176600 16 0010
~~~
  - **RANGE_LOW** : low value del rango, 8 dígitos.
  - **RANGE_HIGHT** : hight value del rango, 8 dígitos.
  - **LEN** : longitud del numero de tarjeta, 2 dígitos.
  - **ID** : identificador único de Tarjeta, 4 dígitos
  
Tenemos un carácter de separación entre cada item, este puede ser cualquier incluso un espacio en blanco, por lo general se usa el símbolo **'~'**.
  
  
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
  - **Nro Tarjeta** : 4517650654628311
  - **Monto** ($124,54): 124.54 
  - **Code** : 123

  
<!--
4817650654628311
~~~ 
Request:
 -------------------------------------------------
| MTID |    Nro Tarjeta     |     Monto    | Code | 
 -------------------------------------------------
| 0200 | 164517650654628311 | 000000012454 | 123  |
 -------------------------------------------------
~~~
-->
 


| **MTID** | **Nro Tarjeta**    | **Monto**    | **Code** | 
|:--------:|:------------------:|:------------:|:--------:|
|   0200   | 164517650654628311 | 000000012454 | 123      |
|          |                    |              |          | 

  
## Response Message
Formato del mensaje Response devuelto por el servidor, todos los campos para este caso deben ser **ASCII**.

~~~ 
Request:
 -------------------
|  MTID  | RespCode |
 -------------------
~~~

  + **MTID** : Message Type Identificator, longitud fija hasta 4 dígitos. Para el Response este debe ser **0210**.
  
  + **RespCode** : El código de respuesta la longitud de este es fija de dos dígitos, código igual a ```00``` significa transacción aprobada. Mientras que un valor distinto a este, para este caso, significa transacción rechazada.
    

Ejemplos:
  - Code : 00, succes
  - Code : 47, no succes
  
| **MTID** | **RespCode** | **Status**  |
|:--------:|:------------:|:------------|
|   0210   |    00        | **SUCCESS** |
|          |              |             | 
|   0210   |  !=00        | **FAILURE** |
 


<!-- 
~~~ 
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
 

    
# Instalaccion python
  - [Instacion python linux](#instacion-python-linux)
  - [Instacion pip linux](#instacion-pip-linux)
  - [Instalaccion dependencias del proyecto](#instalaccion-dependencias-del-proyecto)
  
Para la ejecución de los script debemos tener instalada en el host los siguientes comandos:

  + **python3**
  + **pip3** (gestor de paquetes python, solo es necesario en caso de usar **mypy** para análisis estático de código)

## Instacion python linux
~~~ bash  
  sudo apt update && sudo apt upgrade -y  
  sudo apt install -y python3  
~~~

## Instacion pip linux
~~~ bash  
  sudo apt-get install -y python3-pip
~~~


## Instalaccion dependencias del proyecto
~~~ bash
  # sobre el directorio root del proyecto
  pip3 install --no-cache-dir -r requerimientos.txt
~~~

# Esquema de directorios de la Aplicacion
  
  + **FinancialTransaction.py** : Script principal del proyecto.
  + **files** : Directorio donde se localizan los archivos de Rango y Tarjetas.
  + **PSocket** : Directorio con el modulo para la conexion Host To Host, Stream Socket Client/Server.
  + **Records** : Directorio con el modulo para el parsing de los archivos de Rango y Tarjetas.
  + **readme.md** : este documento 
  + **requerimientos.txt** : Archivo con los package requeridos para el proyecto (para este caso solo **mypy** y si es requerido realizar el análisis con el mismo)
  
  + **Server.py** : Script Python Con el Server, el cual debe ejecutarse previamente antes que el script del proyecto.
  
  
~~~
.
├── files
│   └── local
│       ├── cards.dat
│       └── ranges.dat
│
├── FinancialTransaction.py
│
├── PSocket
│   ├── __init__.py
│   └── Stream.py
│
├── readme.md
├── Records
│   ├── Cards.py
│   ├── Ranges.py
│   └── Records.py
│
├── requerimientos.txt
│
└── Server.py

~~~
    

# Ejecucion del proyecto
  - [Ejecuccion del server](#ejecuccion-del-server)
  - [Ejecuccion Cliente](#ejecuccion-cliente)
  - [Side Client Server down](#side-client-server-down)
  - [Side Client Server timeout](#side-client-server-timeout)

## Ejecuccion del server
Para ejecutar este tenemos las siguientes opciones:

  1. Sin pasar parametros
  ~~~ bash
  python3 Server.py
  Connect Success to Server(ip=0.0.0.0,port=8080,fmt_len=4)
  ~~~

  2. Pasando la Ip y el puerto para el server:
  ~~~ bash
  python3 Server.py 127.0.0.1 3000
  Connect Success to Server(ip=127.0.0.1,port=3000,fmt_len=4)
  ~~~
  
  3. Solo pasando el Puerto:
  ~~~ bash
  python3 Server.py 8080
  Connect Success to Server(ip=0.0.0.0,port=8080,fmt_len=4)
  ~~~
  
Este queda esperando a que un cliente se conecte, al conectarse nos muestra por el prompt la direccion del mismo y cuando el cliente nos envié un mensaje. Imprimara el mismo por pantalla, seguido por el mensaje para el ingreso de una respuesta que se le enviara al cliente, ejemplo:

~~~ bash
  python3 Server.py
Connect Success to Server(ip=0.0.0.0,port=8080,fmt_len=4)
Connect Address Client ('127.0.0.1', 39136)
## mensaje arrivado desde el cliente
Message receive: 0200164517650654628311000000001256123
## Pedido del ingreso de la respuesta a enviar al cliente
Insert CODE (Ctrl+c to end) :00

## recepcion del ACK desde el cliente
End
~~~




## Ejecuccion Cliente
El cliente o el script del proyecto ```FinancialTransaction.py```, al ejecutar el mismo nos pedirá una serie de datos 

  1. Ingresar el Saldo, solo hasta dos dígitos decimales (dos dígitos después del punto decimal), *ex ($124,54): 124.54* 

  2. Ingreso NroTarjeta, *ex: 4517650654628311*

  3. Ingreso de Clave de seguridad (solo 3-Digito), *ex: 123*
  
Si no se insertan los datos correctamente nos debe visualizar por pantalla el error ocurrido y abortar la operación. Si todos los datos fueron cargados satisfactoriamente visualizara por pantalla y enviara la petición al server.

  
Del lado del servidor, al recibir el mensaje nos pedirá ingresar un código de respuesta:
    
  4. Del lado del servidor se recibirá la respuesta con el **MTID 0210** seguida del código:
    - '00' , aprobada ok
    - Distinto de '00' error, trx rechazada.

Side Client:

~~~ bash
  python3 FinancialTransaction.py
Ingrese el monto (hasta 2 decimales Implicitos): 124.54
Ingrese el numero de Tarjeta: 4517650654628311
## Tarjeta localizada y validada
LABEL CARD: BAN Nro 0010
Ingrese el Codigo de Seguridad (hasta 3 digitos): 123
Connect Success to Client(ip=0.0.0.0,port=8080,fmt_len=4)
APROBADA
~~~

Side Server:

~~~ bash
python3 Server.py 8080
Connect Success to Server(ip=0.0.0.0,port=8080,fmt_len=4)
Connect Address Client ('127.0.0.1', 41500)
Message receive: 0200164517650654628311000000012454123
Insert CODE (Ctrl+c to end) :00
End
~~~




## Side Client Server down
~~~ bash
python3 FinancialTransaction.py 
Ingrese el monto (hasta 2 decimales Implicitos): 124.54
Ingrese el numero de Tarjeta: 4517650654628311
LABEL CARD: BAN Nro 0010
Ingrese el Codigo de Seguridad (hasta 3 digitos): 123
Error connect <Client(ip=0.0.0.0,port=8080,fmt_len=4)>: Connection refused
~~~

## Side Client Server Cancel
~~~ bash
python3 FinancialTransaction.py 
Ingrese el monto (hasta 2 decimales Implicitos): 25669.45
Ingrese el numero de Tarjeta: 4517650654628311
LABEL CARD: BAN Nro 0010
Ingrese el Codigo de Seguridad (hasta 3 digitos): 123
Connect Success to Client(ip=0.0.0.0,port=8080,fmt_len=4)
response: 
ERROR DE COMUNICACION, SERVER CLOSE COMUNICATION
~~~

## Side Client Server timeout
~~~ bash
python3 FinancialTransaction.py
Ingrese el monto (hasta 2 decimales Implicitos): 123.45678
Ingrese el numero de Tarjeta: 4517650654628311
LABEL CARD: BAN Nro 0010
Ingrese el Codigo de Seguridad (hasta 3 digitos): 321
Connect Success to Client(ip=0.0.0.0,port=8080,fmt_len=4)
ERROR DE COMUNICACION TIME-OUT
~~~


<!-- 
Ingrese el monto (hasta 2 decimales Implícitos): 124.54
Ingrese el Numero de Tarjeta ( 13 ~ 99 decimales): 4517650654628311
Ingrese el Código de Seguridad (hasta 3 dígitos): 123
El Saldo ingresado es: 12454
El Numero de tarjeta ingresado es: 4517650654628311
El Código de tarjeta ingresado es: 123

Connect Success to Server(ip=0.0.0.0,port=8080,fmt_len=4)
Connect Address Client ('127.0.0.1', 39136)
Message receive: 0200164517650654628311000000001256123
Insert CODE (Ctrl+c to end) :00
End


| 0200 | 16 4517650654628311 | 000000001256 | 123
| 0200 | 16 4517650654628311 | 000000012454 | 123

-->







