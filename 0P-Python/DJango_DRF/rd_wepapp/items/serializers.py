from rest_framework import serializers # type: ignore pylint: disable=import-error
from .models import Item,Seller


class SellerSerializer(serializers.ModelSerializer): # pylint: disable=too-few-public-methods
    '''
    Modelo de la clase para realizar la serializacion de objetos del tipo Seller
    '''
    class Meta: # pylint: disable=too-few-public-methods
        '''
        Definicion de los meta datos para Seller
        '''
        model = Seller
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer): # pylint: disable=too-few-public-methods
    '''
    Modelo de la clase para realizar la serializacion de objetos del tipo Item
    '''
    class Meta: # pylint: disable=too-few-public-methods
        '''
        Definicion de los meta datos para Item
        '''
        model = Item
        fields = '__all__'
