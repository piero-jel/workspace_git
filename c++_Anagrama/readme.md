# Contenido

  + [Anagrama, Descripción del Proyecto](#anagrama)
  
  + [Compilación](#compilacion)
    - [Instalación Red Hat](#instalaccion-red-hat)
    - [Instalación Debian](#instalaccion-debian)
    - [Configuración Makefile](#configuracion-makefile)
 
  + [Examples](#examples)
    - [make all](#make-all)
    - [make new](#make-new)
    - [make run](#make-run)
    - [run executable](#run-executable)

# Anagrama
Programa que permite verificar si dos palabras son un Anagrama, *una palabra es anagrama de otra si las dos tienen las mismas letras, con el mismo número de apariciones, pero en un orden diferente*.


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
    
  4. Setting Arguments ```ARGS``` esta variable nos permite establecer el listado de argumentos que se pasa en la ejecución o depuración del proyecto. 


# Examples
## make all
~~~ bash
make

===========[BEGIN, compiling VERSION: 0, STD_VER: 2020 ]==========

Tamaño del archivo ejecutable formato:
   text    data     bss     dec     hex filename
  43194     856     344   44394    ad6a ./app/Datagram_v0
===========[END, compiling: "Datagram_v0"]==========
~~~

## make new
~~~ bash
make new

===========[ clean files ... ]==========

===========[BEGIN, compiling VERSION: 0, STD_VER: 2020 ]==========

Tamaño del archivo ejecutable formato:
   text    data     bss     dec     hex filename
  43194     856     344   44394    ad6a ./app/Datagram_v0
===========[END, compiling: "Datagram_v0"]==========
~~~

## make run
~~~ bash
make run

===========[BEGIN, compiling VERSION: 0, STD_VER: 2020 ]==========

Tamaño del archivo ejecutable formato:
   text    data     bss     dec     hex filename
  43194     856     344   44394    ad6a ./app/Datagram_v0
===========[END, compiling: "Datagram_v0"]==========

./app/Datagram_v0 ARGS = ''carlos' 'solarc' 'Nacionalista' 'Altisonancia'', CASE = ''
usando la expresion lamda lmb_checkAnagrama()
Datagram <carlos> - <solarc>
No Datagram <Nacionalista> - <Altisonancia>


Usando la funcion checkAnagrama([std::string])
Datagram <carlos> - <solarc>
Datagram <Nacionalista> - <Altisonancia>


Usando la funcion checkAnagrama([char*])
Datagram <carlos> - <solarc>
Datagram <Nacionalista> - <Altisonancia>
~~~

## run executable
~~~ bash
app/Datagram_v0 carlos solarc Nacionalista Altisonancia
usando la expresion lamda lmb_checkAnagrama()
Datagram <carlos> - <solarc>
No Datagram <Nacionalista> - <Altisonancia>


Usando la funcion checkAnagrama([std::string])
Datagram <carlos> - <solarc>
Datagram <Nacionalista> - <Altisonancia>


Usando la funcion checkAnagrama([char*])
Datagram <carlos> - <solarc>
Datagram <Nacionalista> - <Altisonancia>
~~~
