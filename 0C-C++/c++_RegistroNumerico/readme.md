# Contenido

  + [Registro Numerico, Descripción del Proyecto](#registro-numerico)
  
  + [Compilación](#compilacion)
    - [Instalación Red Hat](#instalaccion-red-hat)
    - [Instalación Debian](#instalaccion-debian)
    - [Configuración Makefile](#configuracion-makefile)
 
  + [Examples](#examples)
    - [make all](#make-all)
    - [make new](#make-new)
    - [make run](#make-run)
    - [run executable](#run-executable)

# Registro Numerico
El registro de Numeros se basa en un programa que solicite al usuario el ingreso de numeros enteros y los guarde en un archivo de acuerdo a los siguentes requerimientos:

  + Se solicitara el ingreso de numeros hasta que se ingrese un valor igual a **0** que no debe ser guardado.
  
  + Al finalizar el ingreso se solicitara ingresar el nombre del archivo en el que se desea guardar los numeros.
  
  + El formato a utilizar en el archivo sera de cadenas de 10 caracteres. Para los numeros de tengan menos de 10 caracteres se rellenara con el caracter '0' (del lado izquierdo) hasta completar la cadena.
 
  + Las cadenas deben quedar separadas en el archivo mediante un salto de linea **CRLF** .
  
  + Seinformara si el archivo fue guardado con exito o si fallo y luego terminara la ejecucion del programa.
 


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
  1. Selección de la versión del proyecto ```VERSION```, por defecto '0' tenemos una sola version para este caso.
  2. Selección de la versión del estándar de compilaccion ```STD_VER``` por defecto esta en '2020', que representa el estándar de c++20.
  3. Setting de depuración de memoria ```DEBUG_ON```, por defecto '0'.
    - 0 : Deshabilita las opciones de debug.
    - 1 : Habilita el **sanitize** para el tracking de memoria reservada (monitoreo del Heap) en tiempo de ejecucion.
    - 2 : Habilita solo los Flags de GDB (para ```make debug``` este se establece de forma automatica).
    

# Examples
## make all
~~~ bash
make

===========[BEGIN, compiling VERSION: 0, STD_VER: 2020 ]==========

Tamaño del archivo ejecutable formato:
   text	   data	    bss	    dec	    hex	filename
  25757	   1040	    576	  27373	   6aed	./app/RegistroNumerico_v0
===========[END, compiling: "RegistroNumerico_v0"]==========

~~~

## make new
~~~ bash
make new

===========[ clean files ... ]==========

===========[BEGIN, compiling VERSION: 0, STD_VER: 2020 ]==========

Tamaño del archivo ejecutable formato:
   text	   data	    bss	    dec	    hex	filename
  25757	   1040	    576	  27373	   6aed	./app/RegistroNumerico_v0
===========[END, compiling: "RegistroNumerico_v0"]==========
~~~

## make run
~~~ bash
make run

===========[BEGIN, compiling VERSION: 0, STD_VER: 2020 ]==========

Tamaño del archivo ejecutable formato:
   text	   data	    bss	    dec	    hex	filename
  26083	   1048	    576	  27707	   6c3b	./app/RegistroNumerico_v0
===========[END, compiling: "RegistroNumerico_v0"]==========

./app/RegistroNumerico_v0 ARGS = '', CASE = ''
Ingrese un Registro Numerico de hasta 10 Digitos: 12
Ingrese un Registro Numerico de hasta 10 Digitos: 3215
Ingrese un Registro Numerico de hasta 10 Digitos: 9876543210
Ingrese un Registro Numerico de hasta 10 Digitos: 0
lista de registros:
0000000012
0000003215
9876543210
Ingrese path/name del Archivo donde se volcara el listado de Registro: out/test_01.txt
Registros volcado al archivo out/test_01.txt de forma Sastifactoria

cat out/test_01.txt 
0000000012
0000003215
9876543210
~~~

## run executable
~~~ bash
app/RegistroNumerico_v0 
Ingrese un Registro Numerico de hasta 10 Digitos: 9874563
Ingrese un Registro Numerico de hasta 10 Digitos: 123
Ingrese un Registro Numerico de hasta 10 Digitos: 0
lista de registros:
0009874563
0000000123
Ingrese path/name del Archivo donde se volcara el listado de Registro: out/test_02.txt
Registros volcado al al archivo out/test_02.txt de forma Sastifactoria

cat out/test_02.txt 
0009874563
0000000123
~~~











