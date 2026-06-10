# Contenido

- [Contenido](#contenido)
- [Anagrama](#anagrama)
- [Esquema de directorios de la Aplicacion](#esquema-de-directorios-de-la-aplicacion)
- [Compilacion](#compilacion)
  - [Instalaccion Fedora Red Hat](#instalaccion-fedora-red-hat)
  - [Instalaccion Debian](#instalaccion-debian)
  - [Configuracion Makefile](#configuracion-makefile)
- [Examples](#examples)
  - [make all](#make-all)
  - [make new](#make-new)
  - [make run](#make-run)
  - [run executable](#run-executable)
  - [run unittests](#run-unittests)

# Anagrama
Programa/funciones que permite verificar si dos palabras son un Anagrama.

  > ***Una palabra es anagrama de otra si las dos tienen las mismas letras, con el mismo número de apariciones, pero en un orden diferente***.

# Esquema de directorios de la Aplicacion
``` bash
.
├── app   # directorio donde se generan los ejecutables
│   ├── Datagram_v0
│   └── unittest_Datagram_v0
├── inc   # directorio donde se localizan los header files del proyecto
│   ├── check_anagrama.hpp
│   └── main.hpp
├── out   # directorio donde se colocan los archivos intermedios de la compilacion
│         # 'los object files'
├── src   # Directorio donde localizaremos los sources files
│   ├── check_anagrama.cpp   
│   ├── main.cpp
│   └── unittests.cpp  # Source file con los test case p/unit test. Con su propio main()
│
├── .vscode     # directorio con la configuracion para vscode
├── Makefile    # Archivo con los target de compilacion
└── readme.md   # este readme file

```

  + **app** : Directorio donde se colocara el ejecutable.
  + **inc** : Directorio donde se localizan los header files.
  + **src** : Directorio donde colocamos los source files.
  + **out** : Directorio donde se colocaran los object files, resultado de la compilación.
  + **`.vscode`** : este contiene los `.*json` con path  relativos y setting para depurar el proyecto desde el IDE. 

  + **Makefile** : Archivo con los target de compilación para `make`. 
  + **readme.md** : este documento 
    
  
# Compilacion
Dentro del directorio root tenemos un **Makefile** con los siguientes targets:

  + **`make all`** : default, este compila los sources.
  + **`make clean`** : elimina los objects files y el ejecutable.
  + **`make new`** : ejecuta un clean y vuelve a compilar.
  + **`make run`** : Si no se compilo aun compila los sources y luego ejecuta.
  + **`make debug`** : Este lanza una sesión de gdb para el debug del proyecto.
  + **`make unittests`** : compila y ejecuta el unittest del proyecto.
  
Para que los target anteriores pueda ejecutarse debemos tener instalado en el sistema **`gcc/g++`**, y **make**.

Los target **run** y **debug** tiene habilitado la variable ARGS con la cual le pasamos al ejecutable (o session de GDB) los argumentos.





## Instalaccion Fedora Red Hat
``` bash
sudo dnf update -y
sudo dnf install -y gcc gdb make libasan libubsan gcc gcc-c++
```

## Instalaccion Debian
``` bash
## apt get
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install -y build-essential make gdb

## aptitude
sudo apt update && sudo apt upgrade -y
sudo apt install -y build-essential make gdb
```



  
  
## Configuracion Makefile
La configuración Básica contempla:

  + Selección de la versión del estándar de compilaccion **`STD_VER`** por defecto esta en '2023', que representa el estándar de `c++23`.
  
  + Setting de depuración de memoria **`DEBUG_ON`**, por defecto '0':
    - 0 : Deshabilita las opciones de debug y **sanitize**, opcion por defecto.
    - 1 : Habilita el **sanitize** para el tracking de memoria reservada (monitoreo del Heap) en tiempo de ejecucion.
    - 2 : Habilita solo los Flags de GDB (para **`make debug`** este se establece de forma automatica).
    
  4. Setting Arguments ```ARGS``` esta variable nos permite establecer el listado de argumentos que se pasa en la ejecución o depuración del proyecto. 

  > **Para el unittest se recomienda el estandar STD_VER con valores 2020, 2023 o superiores**.

# Examples
## make all
``` bash
make

===========[BEGIN, compiling VERSION: 0, STD_VER: 2020 ]==========

Tamaño del archivo ejecutable formato:
   text    data     bss     dec     hex filename
  43194     856     344   44394    ad6a ./app/Datagram_v0
===========[END, compiling: "Datagram_v0"]==========
```

## make new
``` bash
make new

===========[ clean files ... ]==========

===========[BEGIN, compiling VERSION: 0, STD_VER: 2020 ]==========

Tamaño del archivo ejecutable formato:
   text    data     bss     dec     hex filename
  43194     856     344   44394    ad6a ./app/Datagram_v0
===========[END, compiling: "Datagram_v0"]==========
```

## make run

```bash
make run
===========[BEGIN, compiling VERSION: 0, STD_VER: 2020 ]==========

Tamaño del archivo ejecutable formato:
   text    data     bss     dec     hex filename
  43194     856     344   44394    ad6a ./app/Datagram_v0
===========[END, compiling: "Datagram_v0"]==========
```

<details>
  <summary><b>run</b></summary>

``` bash
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
```
    
</details>


## run executable
``` bash
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
```

## run unittests
```bash
make unittests 
```

<details>
  <summary><b>unittests</b></summary>

```bash
===========[BEGIN, compiling VERSION: 0, STD_VER: 2020 ]==========

Tamaño del archivo ejecutable formato:
   text    data     bss     dec     hex filename
 108837    1076     368  110281   1aec9 ./app/unittest_Datagram_v0
===========[END, compiling: "unittest_Datagram_v0"]==========


Test ExecuteTestCases, smart pointer
Inicio de la ejecucion Class TestCaseAnagram
checkAnagrama(carlos,solarc)
checkAnagrama(nacionalista,altisonancia)
Run Sucess Method string_ok
checkAnagrama(carlos,alberto)
checkAnagrama(Nacionalista,Altisonancia)
checkAnagrama(Raiz,zi a)
Run Sucess Method string_nok
checkAnagrama(carlos,solarc,true)
checkAnagrama(Nacionalista,Altisonancia,true)
checkAnagrama(CARLOS,carlos,true)
Run Sucess Method string_sensitive
checkAnagrama(carlOs,Alberto,true)
checkAnagrama(internacional,Altisonancia,true)
checkAnagrama(CARLOS,Acaraz,true)
Run Sucess Method string_sensitive_nok
checkAnagrama(carlos,solarc)
checkAnagrama(nacionalista,altisonancia)
Run Sucess Method const_char_ok
checkAnagrama(carlos,alberto)
checkAnagrama(Nacionalista,Altisonancia)
checkAnagrama(Raiz,zi a)
Run Sucess Method const_char_nok
checkAnagrama(carlos,solarc,true)
checkAnagrama(Nacionalista,Altisonancia,true)
checkAnagrama(CARLOS,carlos,true)
Run Sucess Method const_char_sensitive
checkAnagrama(carlOs,Alberto,true)
checkAnagrama(internacional,Altisonancia,true)
checkAnagrama(CARLOS,Acaraz,true)
Run Sucess Method const_char_sensitive_nok
Fin    de la ejecucion Class TestCaseAnagram
Run 8 test case, 8 Success and 0 with error.

Test ExecuteTestCases, current pointer
Inicio de la ejecucion Class TestCaseAnagram
checkAnagrama(carlos,solarc)
checkAnagrama(nacionalista,altisonancia)
Run Sucess Method string_ok
checkAnagrama(carlos,alberto)
checkAnagrama(Nacionalista,Altisonancia)
checkAnagrama(Raiz,zi a)
Run Sucess Method string_nok
checkAnagrama(carlos,solarc,true)
checkAnagrama(Nacionalista,Altisonancia,true)
checkAnagrama(CARLOS,carlos,true)
Run Sucess Method string_sensitive
checkAnagrama(carlOs,Alberto,true)
checkAnagrama(internacional,Altisonancia,true)
checkAnagrama(CARLOS,Acaraz,true)
Run Sucess Method string_sensitive_nok
checkAnagrama(carlos,solarc)
checkAnagrama(nacionalista,altisonancia)
Run Sucess Method const_char_ok
checkAnagrama(carlos,alberto)
checkAnagrama(Nacionalista,Altisonancia)
checkAnagrama(Raiz,zi a)
Run Sucess Method const_char_nok
checkAnagrama(carlos,solarc,true)
checkAnagrama(Nacionalista,Altisonancia,true)
checkAnagrama(CARLOS,carlos,true)
Run Sucess Method const_char_sensitive
checkAnagrama(carlOs,Alberto,true)
checkAnagrama(internacional,Altisonancia,true)
checkAnagrama(CARLOS,Acaraz,true)
Run Sucess Method const_char_sensitive_nok
Fin    de la ejecucion Class TestCaseAnagram
Run 8 test case, 8 Success and 0 with error.
```
 
</details>

