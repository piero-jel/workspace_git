# build module
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
    