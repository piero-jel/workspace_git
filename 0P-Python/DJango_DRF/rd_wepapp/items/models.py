import json
#from django.db import models,utils
from django.db import models # type: ignore pylint: disable=import-error, disable=unused-import


# Create your models here.

class Seller(models.Model):
    '''
        "nickname": "ELECTRO WORLD2",
        "id": 541407353
    '''
    id = models.PositiveBigIntegerField(auto_created=False,primary_key=True)
    nickname = models.CharField(max_length=256)
    def __repr__(self):
        return f"{type(self).__name__}(id={self.id},nickname={self.nickname})"

    def __str__(self):
        return self.__repr__()

    @classmethod
    def json2object(cls,body:str|dict) -> 'Seller':
        '''Factory Method class method that creates and returns an instance of the class
        Params:
            - body string json o dictionary with fields
        
        Return objet Seller
        '''
        if isinstance(body,dict):
            return cls(**body)

        if isinstance(body,str):
            att = json.loads(body)
            return cls(**att)

        raise TypeError(f"{cls}::att2object() type body {type(body)}")


class Item(models.Model):
    '''
        "id": "MLA1458712843",
        "title": "Smartwatch Xiaomi Redmi 5 Lite 1.96 Negro",
        "price": 64999,
        "seller": { },
        "thumbnail": "http://http2.mlstatic.com/D_852209-MLA80100090514_102024-I.jpg",
        "listing_type_id": "gold_special"
    '''
    id = models.CharField(max_length=32,auto_created=False,primary_key=True)
    title = models.CharField(max_length=256)
    price = models.FloatField(default=0.0)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    #thumbnail = models.URLField(blank=True)
    thumbnail = models.CharField(max_length=256)
    listing_type_id = models.CharField(max_length=32)
    def __repr__(self):
        return f"{type(self).__name__}(id={self.id},title={self.title},price={self.price})"

    def __str__(self):
        return self.__repr__()



    @classmethod
    def json2object(cls,body:str|dict = None) -> 'Item':
        '''Factory Method class method that creates and returns an instance of the class
        Params:
            - body string json o dictionary with fields
        
        Return objet Item
        '''
        def veryfy_seller(b:dict)->dict:
            #attr_seller = None if not 'seller' in body else body['seller']
            attr_seller = b.get('seller',None)
            if attr_seller is None:
                return b

            if not isinstance(attr_seller,dict):
                #raise TypeError(f"{cls}::att2object() seller is not object")
                raise TypeError("seller is not object")

            id_attr = attr_seller.get('id',None)
            if id_attr is None:
                raise TypeError("field id not found in seller object")

            if Seller.objects.filter(id=id_attr).exists(): # pylint: disable=no-member
                sel =  Seller.objects.get(id=id_attr) # pylint: disable=no-member
                del b['seller']
                b['seller'] = sel
                return b

            raise ValueError(f"seller<{id_attr}> not found in Data Base")

        if isinstance(body,dict):
            body = veryfy_seller(body)
            return cls(**body)

        if isinstance(body,str):
            att = json.loads(body)
            att = veryfy_seller(att)
            return cls(**att)

        raise TypeError(f"{cls}::att2object() type body {type(body)}")
