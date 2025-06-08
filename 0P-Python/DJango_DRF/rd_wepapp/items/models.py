from django.db import models,utils
import json


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
        #endif
        if isinstance(body,str):
            att = json.loads(body)
            return cls(**att)
        #endif
        raise TypeError(f"{cls}::att2object() type body {type(body)}")
    #endif
#endclass


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
    #enddef

    def __str__(self):
        return self.__repr__()
    #enddef


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
            if(attr_seller is None):
                return b
            #endif
            if(not isinstance(attr_seller,dict)):
                #raise TypeError(f"{cls}::att2object() seller is not object")
                raise TypeError(f"seller is not object")
            #endif
            id = attr_seller.get('id',None)
            #None if not 'id' in attr_seller else attr_seller['idr']
            if(id is None):
                #raise TypeError(f"{cls}::att2object() seller:id not found in body")
                raise TypeError(f"field id not found in seller object")
            #endif
            
            if(Seller.objects.filter(id=id).exists()):
                sel =  Seller.objects.get(id=id)
                del b['seller']
                b['seller'] = sel
                return b
            #endif
            #raise TypeError(f"{cls}::att2object() seller<{id}> not found")
            raise ValueError(f"seller<{id}> not found in Data Base")
        #endif
        if isinstance(body,dict):
            body = veryfy_seller(body)
            return cls(**body)            
        #endif
        if isinstance(body,str):
            att = json.loads(body)
            att = veryfy_seller(att)
            return cls(**att)
        #endif
        raise TypeError(f"{cls}::att2object() type body {type(body)}")
    #endif
#endclass