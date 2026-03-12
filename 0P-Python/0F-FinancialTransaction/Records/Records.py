"""@package docstring
Copyright 2022, Jesus Emanuel Luccioni
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

 1. Redistributions of source code must retain the above copyright notice,
    this list of conditions and the following disclaimer.

 2. Redistributions in binary form must reproduce the above copyright notice,
    this list of conditions and the following disclaimer in the documentation
    and/or other materials provided with the distribution.

 3. Neither the name of the copyright holder nor the names of its
    contributors may be used to endorse or promote products derived from this
    software without specific prior written permission.

THIS SCRIPT IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SCRIPT, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.

\b file Records/Records.py
\b brief definition class base (class abstract, interfaces, etc), for parsing registers file
\b author Jesus Emanuel Luccioni - piero.jel@gmail.com.
\b date Lunes 05 de Mayo de 2022.
\b version 0.0.1.
  
\b Change History:

Author         Date                 Version     Brief
JEL            2022.05.05           0.0.1       Version Inicial

"""
from abc import ABC, abstractmethod

class Record(ABC):
    ''' Clase Base Abstracta para Registros
  
        - mapkey es el dict que contiene el diccionario
          con el nombre de los atributos en funcion de los slice
          para verificar el contenido (si es solo digitos). 
          Si el nombre inicia cono '!' solo usa el slice para
          tomar el string.
    '''
    def __init__(self,mapkey:dict=None):
        self.mp:dict = mapkey # dict or map key value

    @abstractmethod
    def __str__(self):
        '''Para un metodo abstracto forzamos a crear __str__'''
        #pass

    def set(self,v:str):
        ''' setting object from string 
            - v : string value, line in the file
        '''
        if not self.mp:
            return

        if not isinstance(v,str):
            raise TypeError(f'type {type(v)} no permitido')

        for k,s in self.mp.items():
            tmp = v[s]
            if k[0] == '!':
                self.__dict__[k[1:]] = tmp
                continue

            if not tmp.isdigit():
                raise ValueError(f'Part {k} in card register <{tmp}> is not digits')

            self.__dict__[k] = tmp

        return

    @classmethod
    def Parsing(cls,pathfile:str, comment:str='#',encoding:str='utf-8') -> list:
        ''' Class method for parsing file
            - pathfile path/file
            - comment optional, comment caracter in file
        '''
        if not isinstance(pathfile,str):
            raise TypeError(f'type {type(pathfile)} no permitido')

        ret:list = []
        with open(pathfile,'r',encoding=encoding) as f2r:
            for it in f2r:
                if it.startswith((comment,'\n','\r')):
                    continue

                ret.append(cls(it))

        return ret

    @classmethod
    def Predicate(cls,v:str):
        ''' class method Predicate'''
        #pass

    @classmethod
    def Find(cls,value,cont:list|tuple):
        ''' class methos for find'''
        pred = cls.Predicate(value)
        for it in cont:
            if pred(it):
                return it

        return None
