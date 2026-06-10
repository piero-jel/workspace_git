# Contenido

- [**Contenido**](#contenido)
- [**Registro Numerico**](#registro-numerico)
- [**Esquema de directorios de la Aplicacion**](#esquema-de-directorios-de-la-aplicacion)
- [**Compilacion**](#compilacion)
  + [Configuracion Makefile](#configuracion-makefile)
  
- [**Preparación del entorno**](#preparación-del-entorno)
- [**Run Examples**](#examples)
- [**unittests**](#unittests)

# Registro Numerico
El registro de Numeros se basa en un programa que solicite al usuario el ingreso de numeros enteros y los guarde en un archivo de acuerdo a los siguentes requerimientos:

  + Se solicitara el ingreso de numeros hasta que se ingrese un valor igual a **0** que no debe ser guardado.
  
  + Al finalizar el ingreso se solicitara ingresar el nombre del archivo en el que se desea guardar los numeros.
  
  + El formato a utilizar en el archivo sera de cadenas de 10 caracteres. Para los numeros de tengan menos de 10 caracteres se rellenara con el caracter '0' (del lado izquierdo) hasta completar la cadena.
 
  + Las cadenas deben quedar separadas en el archivo mediante un salto de linea **CRLF** .
  
  + Seinformara si el archivo fue guardado con exito o si fallo y luego terminara la ejecucion del programa.
 
# Esquema de directorios de la Aplicacion

<details><summary><b>Tree Directory</b></summary>

```bash
.
├── app  # Directorios de los ejecutables
├── inc  # Directorio con los header files del proyecto
│   ├── main.hpp
│   └── registro.hpp
├── Makefile  # Archivo con los target para compilar y ejecutar
├── out       # Directorio intermedio para la compilación  
├── readme.md # este archivo
└── src       # Directorio con los archivos fuentes
    ├── main.cpp
    ├── registro.cpp
    └── unittests.cpp

```

</details><br>

  + **app** : Directorio donde se colocara el ejecutable.
  + **inc** : Directorio donde se localizan los header files.
  + **src** : Directorio donde colocamos los source files.
  + **Makefile** : Archivo con los target de compilación para ```make```.
  + **out** : Directorio donde se colocaran los object files, resultado de la compilación.
  + **readme.md** : este documento.

Debemos considerar que dentro de los **sources files** tenemos tres archivos importantes:

  - **`src/main.cpp`** archivo principal con el core del proyecto.
  - **`src/unittests.cpp`** los test cases del unit tests.
  
  > Todos ellos con su correspondiente función `main()`, por lo que se aconseja manejar/editar con cuidado el archivo **`Makefile`**, ya que se pueden modificar los filter y se intente compilar combinaciones de estos. Lo que arrojara errores relacionados al comando **`make`**.
  
  
# Compilacion
Dentro del directorio root tenemos un **Makefile** con los siguientes targets:

  + **`make all`** : default, este compila los sources.
  + **`make clean`** : elimina los objects files y el ejecutable.
  + **`make new`** : ejecuta un clean y vuelve a compilar.
  + **`make run`** : Si no se compilo aun compila los sources y luego ejecuta.
  + **`make debug`** : Este lanza una sesión de gdb para el debug del proyecto.
  + **`make unittests`** : Compila solo el codigo correspondiente a los unit tests.
  
Para que los target anteriores pueda ejecutarse se recomienda tener instalado **gcc/g++**, y **make**, de caso contrario debemos instalarlos.

Los target **run** y **debug** tiene habilitado la variable ARGS con la cual le pasamos al ejecutable (o session de GDB) los argumentos.
  
## Configuracion Makefile
La configuración Básica contempla:
  + Selección de la versión del estándar de compilaccion **`STD_VER`** por defecto esta en '2023', que representa el estándar de c++23.
  + Setting de depuración de memoria **`DEBUG_ON`**, por defecto '0':
  
    - 0 : Deshabilita las opciones de debug.
    - 1 : Habilita el **sanitize** para el tracking de memoria reservada (monitoreo del Heap) en tiempo de ejecucion.
    - 2 : Habilita solo los Flags de GDB (para **`make debug`** este se establece de forma automatica).
    
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

# Examples

<details><summary><b>make all</b></summary>
## make all
``` bash
make

===========[BEGIN, compiling VERSION: 0, STD_VER: 2020 ]==========

Tamaño del archivo ejecutable formato:
   text	   data	    bss	    dec	    hex	filename
  25757	   1040	    576	  27373	   6aed	./app/RegistroNumerico_v0
===========[END, compiling: "RegistroNumerico_v0"]==========

```
</details>
<details><summary><b>make new</b></summary>

``` bash
make new

===========[ clean files ... ]==========

===========[BEGIN, compiling VERSION: 0, STD_VER: 2020 ]==========

Tamaño del archivo ejecutable formato:
   text	   data	    bss	    dec	    hex	filename
  25757	   1040	    576	  27373	   6aed	./app/RegistroNumerico_v0
===========[END, compiling: "RegistroNumerico_v0"]==========
```

</details>
<details><summary><b>make run</b></summary>

``` bash
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
```

</details>
<details><summary><b>run executable</b></summary>

``` bash
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
```

</details>
<br>

# unittests
Compilación de los unittests

```bash
make unittests
```

<details>
<summary><b>compile</b></summary>

```bash
make clean
make unittests

==========[ BEGIN, compiling C++ file ./src/registro.cpp ]==========
==========[ END, compiling C++ file ./src/registro.cpp ]==========


==========[ BEGIN, compiling C++ file ./src/unittests.cpp ]==========
==========[ END, compiling C++ file ./src/unittests.cpp ]==========


===========[BEGIN, compiling VERSION: 0, STD_VER: 2020 ]==========

Tamaño del archivo ejecutable formato:
   text    data     bss     dec     hex filename
  82219    1212     368   83799   14757 ./app/unittest_app
===========[END, compiling: "unittest_app"]==========

```
    
</details>


Ejecución de los unittests:

```bash
make unittests_run
```

  > No es necesario ejecutar en secuencia, primero el **`make unittests`** y luego **`make unittests_run`** si solo queremos ejecutar los mismos. Al estar armada las dependencias dentro del makefile con solo ejecutar **`make unittests_run`** se compilara lo necesario para armar el binario correspondiente para luego ejecutarlo.













