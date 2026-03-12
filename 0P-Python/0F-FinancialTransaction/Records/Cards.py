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

\b file Records/Cards.py
\b brief parsing cards registers file
\b author Jesus Emanuel Luccioni - piero.jel@gmail.com.
\b date Lunes 05 de Mayo de 2022.
\b version 0.0.1.
  
\b Change History:

Author         Date                 Version     Brief
JEL            2022.05.05           0.0.1       Version Inicial

"""
from Records.Records import Record

class CardsRegister(Record):
    ''' Defincion del objeto CardsRegister que modela 
        los registros del archivo de tarjetas
        LABEL(12)~ID(4BYTES)
    '''
    def __init__(self,v:str):
        """
        Inicializacion para un objeto del tipo CardsRegister

        :param v: argument descripcion 
        :type v: str
        """
        self.label:str = ''
        self.id:str = ''
        mp:dict = {
            '!label': slice(0,12)
          , 'id':slice(13,17)
        }
        super().__init__(mp)
        super().set(v)

    def __repr__(self):
        ''' representacion formal del objeto mediante un string'''
        return f"{type(self).__name__}(label={self.label:12},id={self.id:04})"

    def __str__(self):
        ''' representacion informal del objeto mediante un string'''
        return f"{self.label:8} {self.id:04}"

    @classmethod
    def Predicate(cls,v):
        def wrapper(item):
            return v.id == item.id

        return wrapper
