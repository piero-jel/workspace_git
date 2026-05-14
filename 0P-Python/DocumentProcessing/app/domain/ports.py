'''
'''
from abc import ABC, abstractmethod




class ProviderInterfaces(ABC):
    ''' Interfaces para los modelos de Provedoores '''

    @abstractmethod
    def do_work(self,data:dict)->dict|list[dict]:
        """
        Metodo que se encarga de realizar el trabajo

        :param data: datos que debe procesar el provider
        :type data: dict

        :return: dato ya procesado
        :rtype: dict | list[dict]
        """        
        #pass
  


class EventPublisher(ABC):
    ''' Define un puerto donde publicaremos el trabajo realizado '''
    @abstractmethod
    def publish(self, header:dict,data:dict):
        """
        Metodo que se encarga de publicar

        :param header: cabecera para el la publicar un resultado
        :type header: dict

        :param data: datos que se debe public
        :type data: dict
        """   
        pass   
        



class EventConsumer(ABC):
    ''' Define un puerto de salida en el dominio '''
    
    @abstractmethod
    def subscribe(self, topic: str):
        pass

    @abstractmethod
    def poll(self, timeout: float):
        pass 