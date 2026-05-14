"""
Copyright 2026, Jesus Emanuel Luccioni
All rights reserved.

This file is part of devops for Open Container (in this case docker )

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

@file providermocks.py
@author Jesus Emanuel Luccioni - jeluccioni@gmail.com.
@brief   ...
@details ...
@version 0.0.3.
@date Jueves 14 de Mayo de 2026.
@pre condiciones que deben cuplirse antes del llamado,
@bug depuracion example: Not all memory is freed when deleting an object of this class.
@warning
@note
@Change History:
Author         Date           Version             Brief
JEL            2026.04.14     0.0.3               Version Inicial no release
"""
# build-in module
from time import sleep
import json

from app.domain.ports import ProviderInterfaces


class ProviderExtraction(ProviderInterfaces):
    """ Proveedor que recibe el contenido crudo, retorna texto extraído."""
    
    def do_work(self, data:dict)->dict:        
        data['Extraction'] = {
            'name' : type(self).__name__,
            'data' : {k:v for k,v in data.items()} 
        }        
        sleep(10)        
        return data
    

class ProviderAnalysis(ProviderInterfaces):
    """ Proveedor que recibe texto extraído, retorna entidades/categorías detectadas"""

    def do_work(self, data:dict)->dict:
        """ """
        sleep(10)
        data['Analysis'] = {
            'name' : type(self).__name__,
            'data' : {k:v for k,v in data.items()} 
        }        
        return data



class ProviderEnrichment(ProviderInterfaces):
    """ Provedor que recibe entidades, retorna metadata enriquecida"""

    def do_work(self, data:dict)->dict:
        """ """
        sleep(10)
        data['Enrichment'] = {
            'name' : type(self).__name__,
            'data' : {k:v for k,v in data.items()} 
        }        
        return data
    
