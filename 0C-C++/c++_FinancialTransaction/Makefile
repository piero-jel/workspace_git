## BEGIN Copyright
# Copyright 2016, Jesus Emanuel Luccioni
# All rights reserved.
#
# This file is part of Workspace.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from this
#    software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#
# POSSIBILITY OF SUCH DAMAGE.
##
## END   Copyright
##
#####################################################################################
## BEGIN configuracion proyecto
#####################################################################################
VERSION ?= 0

## Set Standar de Compilacion {2011,2014,2017,2020}, default value 2011
STD_VER  := 2020

## '1' enable, '0' disable, (!= 1 && != 0) user setting for debug
DEBUG_ON := 0



## para el linker de shared libraries del sistema
## estas son pasadas en flag en barias etapas
# LINKER_FLAGS = -lrt -pthread

## -i : ip
## -p : port
## -r : path/range_file
## -c : path/cards_file
## -t : timeout in ms
##
ifeq ($(VERSION),0)
	APP = FinancialTransaction
	ARGS = -r files/local/ranges.dat -c files/local/cards.dat
#	ARGS = -i 0.0.0.0 -p 8080 -r files/local/ranges.dat -c files/local/cards.dat -t 5000

else ifeq ($(VERSION),1)
	APP = Host2HostServer
	ARGS = 3000

else ifeq ($(VERSION),2)
	APP = FinancialTransaction
	ARGS =

else ifeq ($(VERSION),3)
	APP = FinancialTransaction
	ARGS = 

else
  APP = FinancialTransaction
  ARGS = 

endif


#CPP_FLAGS = -O2
# CPP_FLAGS = -Ofast

#### Set el coompiler family
# COMPILER ?= clang
# COMPILER ?= clang-9
# COMPILER ?= clang-11
# COMPILER ?= clang-12
# COMPILER ?= gcc

## disable para este caso el postfix de version al appname
APP_NAME = $(APP)_v$(VERSION)

#####################################################################################
## END   configuracion proyecto
#####################################################################################
##
##
#####################################################################################
## BEGIN set flags compiles memory track/gdb/glibcxx
###################################################################################
## 
ifeq ($(DEBUG_ON),1)
## enable debug flags
  DEBUG_MEMORY   ?= 1
  DEBUG_GDB      ?= 1
  DEBUG_GLIBCXX  ?= 1
else ifeq ($(DEBUG_ON),0)
## disable debug flags
  DEBUG_MEMORY   ?= 0
  DEBUG_GDB      ?= 0
  DEBUG_GLIBCXX  ?= 0
else
## set user debug flags
  DEBUG_MEMORY   ?= 0
  DEBUG_GDB      ?= 1
  DEBUG_GLIBCXX  ?= 1
endif
#####################################################################################
## END   set flags compiles memory track/gdb/glibcxx
###################################################################################
##
##
#####################################################################################
## BEGIN set vars
#####################################################################################
AR        = $(CROSS_COMPILER)ar
SIZE      = $(CROSS_COMPILER)size
GETASM	  = $(CROSS_COMPILER)objdump -S

ifeq ($(COMPILER),clang)
CC        = clang
CCPP      = clang++
# FLAGS = -stdlib=libc++ -v
FLAGS = -stdlib=libstdc++
# FLAGS = -v

else ifeq ($(COMPILER),clang-9)
CC        = clang-9
CCPP      = clang++-9
else ifeq ($(COMPILER),clang-11)
CC        = clang-11
CCPP      = clang++-11
else ifeq ($(COMPILER),clang-12)
CC        = clang-12
CCPP      = clang++-12
else ifeq ($(COMPILER),gcc)
CC        = gcc
CCPP      = g++
else
CC        = $(CROSS_COMPILER)gcc
CCPP      = $(CROSS_COMPILER)g++
LD        = $(CROSS_COMPILER)ld
endif




SRC_PATH = ./src
INC_PATH = ./inc
OBJ_PATH = ./out
APP_PATH = ./app

### source file -> *.cpp, *.cxx, *.cc, *.C
CPP_FILES = $(wildcard $(SRC_PATH)/*.cpp)
CXX_FILES += $(wildcard $(SRC_PATH)/*.cxx)
CCC_FILES += $(wildcard $(SRC_PATH)/*.cc)
CC_FILES += $(wildcard $(SRC_PATH)/*.C)

### 
OBJ_FILES = $(addprefix $(OBJ_PATH)/,$(notdir $(CPP_FILES:.cpp=.o)))
OBJ_FILES += $(addprefix $(OBJ_PATH)/,$(notdir $(CXX_FILES:.cxx=.o)))
OBJ_FILES += $(addprefix $(OBJ_PATH)/,$(notdir $(CCC_FILES:.cc=.o)))
OBJ_FILES += $(addprefix $(OBJ_PATH)/,$(notdir $(CC_FILES:.C=.o)))
PROJECT_OBJS := $(notdir $(OBJ_FILES))

INCLUDES = $(addprefix -I, $(INC_PATH))
# INCLUDES += /usr/include/c++/9
## BEGIN Init Flag
# FLAGS = -Wall 
# FLAGS = -ansi -pedantic -Wall -Wextra -Weffc++
## quit -pedantic for disable warning -Wvariadic-macros
FLAGS = -ansi -Wall -Wextra -Weffc++

## agregamos el link para las librerias de posix thread/timer
FLAGS += $(LINKER_FLAGS)
# FLAGS += -Wno-unknown-pragmas


ifeq ($(STD_VER),2011)
  FLAGS += -std=gnu++11
  
else ifeq ($(STD_VER),2014)
  FLAGS += -std=gnu++14

else ifeq ($(STD_VER),2017)  
## GCC Version 8 support to c++17
  FLAGS += -std=gnu++17
  
else ifeq ($(STD_VER),2020)
## c++20
# FLAGS += -std=gnu++2a # version preliminar 'release c++20'
  FLAGS += -std=gnu++20

else ifeq ($(STD_VER),2023)
## c++23, version preliminar
  FLAGS += -std=c++2b 
else
  FLAGS += -std=gnu++11
endif



ifeq ($(DEBUG_GDB),1)
FLAGS += -g -DNDEBUG
endif


ifeq ($(DEBUG_MEMORY),1)
LDFLAGS = -fsanitize=address,leak -pg
endif

ifeq ($(DEBUG_GLIBCXX),1)
  ifeq ($(COMPILER),clang-13)
    FLAGS += -std=c++17 -fsanitize=address -fsanitize=undefined
  else
    FLAGS += -D_GLIBCXX_DEBUG
  endif
endif

SYMBOLS = -DVERSION=$(VERSION) -D__STD_VER__=$(STD_VER)
# FLAGS += -stdlib=libc++

# FLAGS += -O1 -g -fsanitize=address -fno-omit-frame-pointer -v

# FLAGS += -fsanitize-link-c++-runtime
# FLAGS += -O0 -g -fsanitize=undefined -fno-omit-frame-pointer -v
FLAGS += $(CPP_FLAGS)
LDFLAGS += $(LINKER_FLAGS)

## END   Init Flag
#####################################################################################
## END   set vars
#####################################################################################

## BEGIN all
all :
	@make $(APP_NAME) --no-print-directory	
## END   all

## BEGIN export file path, *.cpp, *.cxx, *.cc, *.C
vpath %.o $(OBJ_PATH)
vpath %.cpp $(SRC_PATH)
vpath %.cxx $(SRC_PATH)
vpath %.cc $(SRC_PATH)
vpath %.C $(SRC_PATH)


## END   export file path

## BEGIN compiling cpp and cxx files
%.o : %.cpp
# 	@echo "\n==========[ BEGIN, compiling C++ file $< ]=========="
	@$(CCPP) $(SYMBOLS) $(FLAGS) $(INCLUDES) -c $< -o $(OBJ_PATH)/$@
	@$(CCPP) $(SYMBOLS) $(FLAGS) $(INCLUDES) -c $< -MM > $(OBJ_PATH)/$(@:.o=.d)
# 	@echo "==========[ END, compiling C++ file $< ]==========\n"

%.o : %.cxx
# 	@echo "\n==========[ BEGIN, compiling C++ file $< ]=========="
	@$(CCPP) $(SYMBOLS) $(FLAGS) $(INCLUDES) -c $< -o $(OBJ_PATH)/$@
	@$(CCPP) $(SYMBOLS) $(FLAGS) $(INCLUDES) -c $< -MM > $(OBJ_PATH)/$(@:.o=.d)
# 	@echo "==========[ END, compiling C++ file $< ]==========\n"

%.o : %.cc
# 	@echo "\n==========[ BEGIN, compiling C++ file $< ]=========="
	@$(CCPP) $(SYMBOLS) $(FLAGS) $(INCLUDES) -c $< -o $(OBJ_PATH)/$@
	@$(CCPP) $(SYMBOLS) $(FLAGS) $(INCLUDES) -c $< -MM > $(OBJ_PATH)/$(@:.o=.d)
# 	@echo "==========[ END, compiling C++ file $< ]==========\n"

%.o : %.C
# 	@echo "\n==========[ BEGIN, compiling C++ file $< ]=========="
	@$(CCPP) $(SYMBOLS) $(FLAGS) $(INCLUDES) -c $< -o $(OBJ_PATH)/$@
	@$(CCPP) $(SYMBOLS) $(FLAGS) $(INCLUDES) -c $< -MM > $(OBJ_PATH)/$(@:.o=.d)
# 	@echo "==========[ END, compiling C++ file $< ]==========\n"
## END   compiling cpp and cxx files

## BEGIN clean target
clean:
	@echo "\n===========[ clean files ... ]=========="
	@rm -f $(OBJ_PATH)/*.*
	@rm -f $(APP_PATH)/$(APP_NAME)
## END   clean target

## BEGIN new target FIXME debemos independizzar del header
new: clean
	@make all --no-print-directory
## END   new target	

## BEGIN APP_NAME target
$(APP_NAME): $(PROJECT_OBJS)
	@echo "\n===========[BEGIN, compiling VERSION: $(VERSION), STD_VER: $(STD_VER) ]=========="
	@$(CCPP) -o $(APP_PATH)/$(APP_NAME) $(OBJ_FILES) $(LDFLAGS)
	@echo "\nTamaño del archivo ejecutable formato:"
	@$(SIZE) -B $(APP_PATH)/$(APP_NAME)
	@echo "===========[END, compiling: \"$(APP_NAME)\"]==========\n"
## END   APP_NAME target

## BEGIN info target
info:
	@echo "CPP_FILES    : $(CPP_FILES)"
	@echo "CXX_FILES    : $(CXX_FILES)"
	@echo "CCC_FILES    : $(CCC_FILES)"
	@echo "CC_FILES     : $(CC_FILES)"
	@echo "OBJ_FILES    : $(OBJ_FILES)"
	@echo "PROJECT_OBJS : $(PROJECT_OBJS)"
	@echo "FLAGS        : $(FLAGS)"
	@echo "APP_NAME     : $(APP_NAME)"
	@echo "INCLUDES     : $(INCLUDES)"
	@echo "hpp          : $(notdir $(wildcard $(INC_PATH)/*.hpp))"
## END   info target	


## BEGIN run target
run:
	@make all --no-print-directory
	@echo "$(APP_PATH)/$(APP_NAME) ARGS = '$(ARGS)', CASE = '$(CASE)'"
	@$(APP_PATH)/$(APP_NAME) $(ARGS)
	
nrun: new
	@$(APP_PATH)/$(APP_NAME) $(ARGS)
## END   run target

## BEGIN debug target
debug: 
	@make new DEBUG_GDB=1 --no-print-directory
	@gdb --args $(APP_PATH)/$(APP_NAME)$(EXT_APP) $(ARGS)
## END   debug target


## BEGIN debug_core target
## para el core dump, comando utilies:
## bt          : (backtrace ver el contenido de la pila de ejecucion)
## frame <Nro> : cambio de contexto 
## list        : para listar el codigo en el frame
debug_core: 
	@make new DEBUG_GDB=1 --no-print-directory
	@gdb $(APP_PATH)/$(APP_NAME)$(EXT_APP) $(CORE_DUMP_FILE)
## END   debug_core target

## BEGIN get asm 
getasm:
	@$(GETASM) $(APP_PATH)/$(APP_NAME)
	
ngetasm: new
	@$(GETASM) $(APP_PATH)/$(APP_NAME)
## END   get asm
## BEGIN help target
help:
	@echo "\n===========[BEGIN, HELP: ]=========="
	@echo "\tmake all          : compila los archivos que cambiaron su estado"
	@echo "\tmake new          : Realiza un clean y vuelve a compialr todo los archivos"
	@echo "\tmake clean        : Elimina todos los archivos generados incluyendo la aplicacion"
	@echo "\tmake run          : Ejecuta la aplicacion"
	@echo "\tmake nrun         : Invoca el target new y luego Ejecuta la aplicacion"
	@echo "\tmake info         : Muestra informacion sobre la configuracion actual del proyecto"
	@echo "\tmake debug        : Inicia la secion de depuracion con GDB GNU DebuG"
	@echo "\tmake debug_core   : Idem a debug mas el contexto para Core Dump"
	@echo "\tmake <Target> ARGS=\"Lista de Arg\" set ARG para los target run, debug"
	@echo "\tmake <Target> DEBUG_GDB= { 1 | 0 } Enable/disable GDB"
	@echo "\tmake <Target> DEBUG_MEMORY= { 1 | 0 } Enable/disable Mmeory Trace Satinizer"
	@echo "\n===========[END  , HELP: ]==========\n"	
## END   help target
