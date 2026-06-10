# Contenido

- [**Contenido**](#contenido)
- [**Unit test utilstr**](#unit-test-utilstr)
- [**Esquema de directorios de la Aplicación**](#esquema-de-directorios-de-la-aplicación)
- [**Compilación**](#compilación)
  + [Configuración Makefile](#configuración-makefile) 
- [**Preparación del entorno**](#preparación-del-entorno)
- [**Examples**](#examples)
  

# Unit test utilstr
Aplicación de test unitarios al conjunto de funciones contenidas sobre el **`namespace utilstr`**. En este podemos ver ejemplos de como utilizar e implementar los test unitarios definidos en el **`namespase unittest`** (Definición de clases para desplegar test unitarios, todas sobre header files y sin librerías de terceros). 
   
# Esquema de directorios de la Aplicación

<details><summary><b>Tree Directory</b></summary>

```bash
.
├── app  # Directorios de los ejecutables
├── inc  # Directorio con los header files del proyecto
│   └── main.hpp
├── Makefile  # Archivo con los target para compilar y ejecutar
├── out       # Directorio intermedio para la compilación  
├── readme.md # este archivo
└── src       # Directorio con los archivos fuentes
    └── main.cpp
```

</details><br>

  + **app** : Directorio donde se colocara el ejecutable.
  + **inc** : Directorio donde se localizan los header files.
  + **src** : Directorio donde colocamos los source files.
  + **Makefile** : Archivo con los target de compilación para **`make`**.
  + **out** : Directorio donde se colocaran los object files, resultado de la compilación.
  + **readme.md** : este documento.

  
# Compilación
Dentro del directorio root tenemos un **Makefile** con los siguientes targets:

  + **`make all`** : default, este compila los sources.
  + **`make clean`** : elimina los objects files y el ejecutable.
  + **`make new`** : ejecuta un clean y vuelve a compilar.
  + **`make run`** : Si no se compilo aun compila los sources y luego ejecuta.
  + **`make debug`** : Este lanza una sesión de gdb para el debug del proyecto.
    
Para que los target anteriores pueda ejecutarse se recomienda tener instalado **gcc/g++**, y **make**, de caso contrario debemos instalarlos.

Los target **run** y **debug** tiene habilitado la variable **`ARGS`** con la cual le pasamos al ejecutable (o session de GDB) los argumentos.

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


  
  
## Configuración Makefile
La configuración Básica contempla:
  + Selección de la versión del estándar de compilaccion **`STD_VER`** por defecto esta en '2023', que representa el estándar de c++23.
  + Setting de depuración de memoria **`DEBUG_ON`**, por defecto '0':
  
    - 0 : Deshabilita las opciones de debug.
    - 1 : Habilita el **sanitize** para el tracking de memoria reservada (monitoreo del Heap) en tiempo de ejecucion.
    - 2 : Habilita solo los Flags de GDB (para **`make debug`** este se establece de forma automatica).
    
> **Se recomienda el estandar STD_VER con valores 2020, 2023 o superiores**.

# Examples

<details><summary style="font-weight: bold; font-size: 14px;"><b>make all</b></summary>

``` bash
make
# o especificando el target all
make all

==========[ BEGIN, compiling C++ file ./src/main.cpp ]==========
==========[ END, compiling C++ file ./src/main.cpp ]==========


===========[BEGIN, compiling VERSION: 0, STD_VER: 2023 ]==========

Tamaño del archivo ejecutable formato:
   text    data     bss     dec     hex filename
 192964    1132     368  194464   2f7a0 ./app/unittest_utilstr
===========[END, compiling: "unittest_utilstr"]==========

```

</details>
<details><summary style="font-weight: bold; font-size: 14px;"><b>make new</b></summary>

``` bash
make new

==========[ BEGIN, compiling C++ file ./src/main.cpp ]==========
==========[ END, compiling C++ file ./src/main.cpp ]==========


===========[BEGIN, compiling VERSION: 0, STD_VER: 2023 ]==========

Tamaño del archivo ejecutable formato:
   text    data     bss     dec     hex filename
 192964    1132     368  194464   2f7a0 ./app/unittest_utilstr
===========[END, compiling: "unittest_utilstr"]==========

```

</details>
<details><summary style="font-weight: bold; font-size: 14px;"><b>make run</b></summary>

``` bash
make run

==========[ BEGIN, compiling C++ file ./src/main.cpp ]==========
==========[ END, compiling C++ file ./src/main.cpp ]==========


===========[BEGIN, compiling VERSION: 0, STD_VER: 2023 ]==========

Tamaño del archivo ejecutable formato:
   text    data     bss     dec     hex filename
 192964    1132     368  194464   2f7a0 ./app/unittest_utilstr
===========[END, compiling: "unittest_utilstr"]==========

./app/unittest_utilstr ARGS = '', CASE = ''

Test ExecuteTestCases
Run Sucess Method split_two_string_nf
Run Sucess Method split_two_string_v1
s1: <ColumnA = 100 > | s2: < ColumB = 100> Run Sucess Method split_two_string_v2
s1: <ColumnA = 100> | s2: <ColumB = 100> Run Sucess Method split_two_string_v3
s1: <ColumnA=100> | s2: <ColumB=100> Run Sucess Method split_two_string_v4
Run Sucess Method split_two_string_v5
Run Sucess Method split_two_string_v6
Run Sucess Method split_two_string_v7
Run Sucess Method split_two_string_v8
Run Sucess Method split_two_char_nf
Run Sucess Method split_two_char_v1
Run Sucess Method split_two_char_v2
Run Sucess Method split_two_char_v3
Run Sucess Method split_two_char_v4
Run Sucess Method split_two_char_v5
Run Sucess Method split_two_char_v6
Run Sucess Method split_two_char_v7
Run Sucess Method split_two_char_v8

Inicio de la ejecucion Class SplitString
Run Sucess Method split_string_not_found
Run Sucess Method split_string_v1
Run Sucess Method split_string_v2
Run Sucess Method split_string_v3
Run Sucess Method split_string_v4
Run Sucess Method split_string_v5
Run Sucess Method split_string_v6
Run Sucess Method split_string_v7
Run Sucess Method split_char_not_found
Run Sucess Method split_char_v1
Run Sucess Method split_char_v2
Run Sucess Method split_char_v3
Run Sucess Method split_char_v4
Run Sucess Method split_char_v5
Run Sucess Method split_char_v6
Run Sucess Method split_char_v7
Fin    de la ejecucion Class SplitString


Inicio de la ejecucion Class SplitStringInArray
a1: : ["","","",""]     Run Sucess Method split_string_not_found
Run Sucess Method split_string_v1
Run Sucess Method split_string_v2
Run Sucess Method split_string_v3
Run Sucess Method split_string_v4
Run Sucess Method split_string_v5
Run Sucess Method split_string_v6
Run Sucess Method split_string_v7
a1: : ["","","",""]     Run Sucess Method split_char_not_found
Run Sucess Method split_char_v1
Run Sucess Method split_char_v2
Run Sucess Method split_char_v3
Run Sucess Method split_char_v4
Run Sucess Method split_char_v5
Run Sucess Method split_char_v6
Run Sucess Method split_char_v7
Fin    de la ejecucion Class SplitStringInArray


Inicio de la ejecucion Class SplitToUpprtAndToLowe
Run Sucess Method to_upper_v1
Run Sucess Method to_upper_v2
Run Sucess Method to_lower_v1
Run Sucess Method to_lower_v2
s1: hola COMO estas     Run Sucess Method to_string_v1
p1: ( 1; 2; 3 ) s1: ( 1; 2; 3 ) Run Sucess Method to_string_v2
Fin    de la ejecucion Class SplitToUpprtAndToLowe


Inicio de la ejecucion Class JoinCont
Run Sucess Method vct_join_v1
Run Sucess Method vct_join_v2
Run Sucess Method vct_join_v3
Run Sucess Method vct_join_v4
Run Sucess Method arr_join_v1
Fin    de la ejecucion Class JoinCont


Inicio de la ejecucion Class ReplaceStr
Run Sucess Method replace_string_v1
Run Sucess Method replace_string_v2
Run Sucess Method replace_string_v3
Run Sucess Method replace_char_v1
Run Sucess Method replace_char_v2
Run Sucess Method replace_char_v3
Run Sucess Method replace_string_nf_v1
Run Sucess Method replace_string_nf_v2
Run Sucess Method replace_char_nf_v1
Run Sucess Method replace_char_nf_v2
Fin    de la ejecucion Class ReplaceStr

Run 71 test case, 71 Success and 0 with error.
```
    
</details>
<details><summary style="font-weight: bold; font-size: 14px;"><b>run executable</b></summary>

``` bash
make
./app/unittest_utilstr 

Test ExecuteTestCases
Run Sucess Method split_two_string_nf
Run Sucess Method split_two_string_v1
s1: <ColumnA = 100 > | s2: < ColumB = 100> Run Sucess Method split_two_string_v2
s1: <ColumnA = 100> | s2: <ColumB = 100> Run Sucess Method split_two_string_v3
s1: <ColumnA=100> | s2: <ColumB=100> Run Sucess Method split_two_string_v4
Run Sucess Method split_two_string_v5
Run Sucess Method split_two_string_v6
Run Sucess Method split_two_string_v7
Run Sucess Method split_two_string_v8
Run Sucess Method split_two_char_nf
Run Sucess Method split_two_char_v1
Run Sucess Method split_two_char_v2
Run Sucess Method split_two_char_v3
Run Sucess Method split_two_char_v4
Run Sucess Method split_two_char_v5
Run Sucess Method split_two_char_v6
Run Sucess Method split_two_char_v7
Run Sucess Method split_two_char_v8

Inicio de la ejecucion Class SplitString
Run Sucess Method split_string_not_found
Run Sucess Method split_string_v1
Run Sucess Method split_string_v2
Run Sucess Method split_string_v3
Run Sucess Method split_string_v4
Run Sucess Method split_string_v5
Run Sucess Method split_string_v6
Run Sucess Method split_string_v7
Run Sucess Method split_char_not_found
Run Sucess Method split_char_v1
Run Sucess Method split_char_v2
Run Sucess Method split_char_v3
Run Sucess Method split_char_v4
Run Sucess Method split_char_v5
Run Sucess Method split_char_v6
Run Sucess Method split_char_v7
Fin    de la ejecucion Class SplitString


Inicio de la ejecucion Class SplitStringInArray
a1: : ["","","",""]     Run Sucess Method split_string_not_found
Run Sucess Method split_string_v1
Run Sucess Method split_string_v2
Run Sucess Method split_string_v3
Run Sucess Method split_string_v4
Run Sucess Method split_string_v5
Run Sucess Method split_string_v6
Run Sucess Method split_string_v7
a1: : ["","","",""]     Run Sucess Method split_char_not_found
Run Sucess Method split_char_v1
Run Sucess Method split_char_v2
Run Sucess Method split_char_v3
Run Sucess Method split_char_v4
Run Sucess Method split_char_v5
Run Sucess Method split_char_v6
Run Sucess Method split_char_v7
Fin    de la ejecucion Class SplitStringInArray


Inicio de la ejecucion Class SplitToUpprtAndToLowe
Run Sucess Method to_upper_v1
Run Sucess Method to_upper_v2
Run Sucess Method to_lower_v1
Run Sucess Method to_lower_v2
s1: hola COMO estas     Run Sucess Method to_string_v1
p1: ( 1; 2; 3 ) s1: ( 1; 2; 3 ) Run Sucess Method to_string_v2
Fin    de la ejecucion Class SplitToUpprtAndToLowe


Inicio de la ejecucion Class JoinCont
Run Sucess Method vct_join_v1
Run Sucess Method vct_join_v2
Run Sucess Method vct_join_v3
Run Sucess Method vct_join_v4
Run Sucess Method arr_join_v1
Fin    de la ejecucion Class JoinCont


Inicio de la ejecucion Class ReplaceStr
Run Sucess Method replace_string_v1
Run Sucess Method replace_string_v2
Run Sucess Method replace_string_v3
Run Sucess Method replace_char_v1
Run Sucess Method replace_char_v2
Run Sucess Method replace_char_v3
Run Sucess Method replace_string_nf_v1
Run Sucess Method replace_string_nf_v2
Run Sucess Method replace_char_nf_v1
Run Sucess Method replace_char_nf_v2
Fin    de la ejecucion Class ReplaceStr

Run 71 test case, 71 Success and 0 with error.


```
    
</details>

