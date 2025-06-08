from django.test import TestCase
from django.db import utils
from .models import Item,Seller
from .serializers import ItemSerializer,SellerSerializer
import json

''' 
    python3 manage.py test -v 2 items.tests_models
'''

# Create your tests here.
attr_seller:dict = {
    "nickname": "SellerTest",
    "id": 237004002253
}

attr_item:dict = {
    "title": "Titulo test Item",
    "price": 29449.50,    
    "id": "TEST-ITEM123456789",
    "thumbnail": "http://",
    "listing_type_id": "gold_special"
}

attr_item_json:str = '''{
    "title": "Titulo test Item",
    "price": 29449.50,    
    "id": "TEST-ITEM123456789",
    "thumbnail": "http://",
    "listing_type_id": "gold_special",
    "seller": {
        "nickname": "SellerTest",
        "id": 237004002253
    }
}'''

class TestModelSeller(TestCase):
    def test_create_seller(self):
        '''Test Create Seller'''
        seller = Seller(**attr_seller)
        seller.save()
        self.assertTrue(Seller.objects.filter(id=attr_seller['id']).exists())
        sel = Seller.objects.get(id=attr_seller['id'])        
        self.assertEqual(sel.nickname, attr_seller['nickname'])
        self.assertEqual(sel.id, attr_seller['id'])
        self.assertEqual(str(sel), f"{type(sel).__name__}(id={sel.id},nickname={sel.nickname})")
    #enddef

    def test_create_seller_raise_id_str(self):
        '''Test Create Seller with Raise exception, id str'''
        attr:dict = {
            "nickname": "SellerTest",
            "id": 'ABCDEF123'
        }
        
        seller = Seller(**attr)
        with self.assertRaises(ValueError):
            seller.save()
        #endwith        
    #enddef

    def test_create_seller_nickname_int(self):
        '''Creacion de un seller con un nickname numerico'''
        attr:dict = {
            "nickname": 9876543210,
            "id": 9876543210
        }
        seller = Seller(**attr)
        seller.save()
        self.assertNotEqual(attr,SellerSerializer(Seller.objects.get(id=attr['id'])).data)
        attr['nickname'] = str(attr['nickname'])
        self.assertEqual(attr,SellerSerializer(Seller.objects.get(id=attr['id'])).data)
    #enddef
        
    def test_serialize_one_seller(self):
        '''Test Serialize one Seller'''
        seller = Seller(**attr_seller)        
        self.assertEqual(attr_seller,SellerSerializer(seller).data)
    #enddef

    def test_serialize_list_seller(self):
        '''Test Serialize list of Seller'''
        lst_attr_seller = []
        for idx in range(1,10):
            it_attr_seller = {"nickname": f'{attr_seller["nickname"]}{idx}',"id":attr_seller['id']+idx}
            Seller(**it_attr_seller).save()
            lst_attr_seller.append(it_attr_seller)            
        #endfor
        ## serializacion de todos los registros creados
        self.assertEqual(lst_attr_seller,SellerSerializer(Seller.objects.all(),many=True).data) 
    #enddef

    def test_create_list_seller(self):
        '''Test Create list of Seller'''
        lst_attr_seller = []
        for idx in range(1,10):
            it_attr_seller = {"nickname": f'{attr_seller["nickname"]}{idx}',"id":attr_seller['id']+idx}
            sel = Seller(**it_attr_seller)
            sel.save()
            lst_attr_seller.append(it_attr_seller)
            ## serializacion de un registro
            self.assertEqual(it_attr_seller,SellerSerializer(sel).data)
            self.assertTrue(Seller.objects.filter(id=sel.id).exists())
        #endfor
        ## serializacion de todos los registros creados
        self.assertEqual(lst_attr_seller,SellerSerializer(Seller.objects.all(),many=True).data)        
    #enddef

    def test_delete_one_seller(self):
        '''Test Delete Seller'''
        Seller(**attr_seller).save()
        self.assertTrue(Seller.objects.filter(id=attr_seller['id']).exists())
        Seller.objects.get(id=attr_seller['id']).delete()
        self.assertFalse(Seller.objects.filter(id=attr_seller['id']).exists())
    #enddef

    def test_delete_all_seller(self):
        '''Test delete all register from table Seller'''
        lst_attr_seller = []
        for idx in range(1,10):
            it_attr_seller = {"nickname": f'{attr_seller["nickname"]}{idx}',"id":attr_seller['id']+idx}
            Seller(**it_attr_seller).save()
            lst_attr_seller.append(it_attr_seller)            
        #endfor
        ## serializacion de todos los registros creados
        self.assertEqual(lst_attr_seller,SellerSerializer(Seller.objects.all(),many=True).data)
        Seller.objects.all().delete()
        self.assertEqual(len(Seller.objects.all()),0)
    #enddef
#endclass


class TestModelSeller_json2object(TestCase):
    def test_create_seller(self):
        '''Test Create Seller from str json'''
        attr_json = json.dumps(attr_seller)
        seller = Seller.json2object(attr_json)
        seller.save()
        self.assertTrue(Seller.objects.filter(id=seller.id).exists())
        sel = Seller.objects.get(id=attr_seller['id'])        
        self.assertEqual(sel.nickname, attr_seller['nickname'])
        self.assertEqual(sel.id, attr_seller['id'])
    #enddef

    def test_try_create_seller_error_type(self):
        '''Test Create Seller from str json'''
        attr_json = []
        with self.assertRaises((ValueError,TypeError)):
            Seller.json2object(attr_json).save()        
    #enddef
    
    def test_create_seller_raise_id_str(self):
        '''Test Create Seller with Raise exception, id str'''
        attr_json = '''{
            "nickname": "SellerTest",
            "id": "ABCDEF123"
        }'''
        
        seller = Seller.json2object(attr_json)
        with self.assertRaises((TypeError,ValueError)):
            seller.save()
        #endwith        
    #enddef
    
    def test_create_seller_nickname_int(self):
        '''Creacion de un seller con un nickname numerico'''
        attr_json = '''{
            "nickname": 9876543210,
            "id": 9876543210
        }'''
        attr = json.loads(attr_json)
        seller = Seller.json2object(attr_json)
        seller.save()
        self.assertNotEqual(attr,SellerSerializer(Seller.objects.get(id=attr['id'])).data)
        attr['nickname'] = str(attr['nickname'])
        self.assertEqual(attr,SellerSerializer(Seller.objects.get(id=attr['id'])).data)
    #enddef
    
    def test_serialize_one_seller(self):
        '''Test Serialize one Seller'''
        attr_json = json.dumps(attr_seller)
        seller = Seller.json2object(attr_json)        
        self.assertEqual(attr_seller,SellerSerializer(seller).data)
    #enddef

    def test_delete_one_seller(self):
        '''Test Delete Seller'''
        attr_json = json.dumps(attr_seller)
        Seller.json2object(attr_json).save()
        self.assertTrue(Seller.objects.filter(id=attr_seller['id']).exists())
        Seller.objects.get(id=attr_seller['id']).delete()
        self.assertFalse(Seller.objects.filter(id=attr_seller['id']).exists())
    #enddef
#endclass

class TestModelItem(TestCase):
    def setUp(self):
        self.seller = Seller(**attr_seller)
        self.seller.save()
        #self.assertTrue(Seller.objects.filter(id=attr_seller['id']).exists())
        self.attr_item = attr_item.copy()
        self.attr_item['seller'] = self.seller
    #endif

    def test_create_item(self):
        '''Test create Item'''
        item = Item(**self.attr_item)
        item.save()
        self.assertTrue(Item.objects.filter(id=self.attr_item['id']).exists())
        self.attr_item['seller'] = self.seller.id
        self.assertEqual(self.attr_item,ItemSerializer(Item.objects.get(id=self.attr_item['id'])).data)
        self.assertEqual(str(item), f"{type(item).__name__}(id={item.id},title={item.title},price={item.price})")
    #enddef

    def test_create_item_id_int(self):
        '''Test Create Item con id entero no str'''        
        self.attr_item['id'] = 9876543219876  
        Item(**self.attr_item).save()
        self.attr_item['seller'] = self.seller.id
        self.assertNotEqual(self.attr_item,ItemSerializer(Item.objects.get(id=str(self.attr_item['id']))).data)
        self.attr_item['id'] = str(self.attr_item['id'])
        self.assertEqual(self.attr_item,ItemSerializer(Item.objects.get(id=self.attr_item['id'])).data)
    #enddef

    def test_create_item_raise_without_seller(self):
        '''Test Create Item, raise django.db.utils.IntegrityError, sin seller'''        
        with self.assertRaises(utils.IntegrityError):
            Item(**attr_item).save()
        #endwith        
    #enddef

    def test_create_seller_nickname_int(self):
        '''Creacion de un seller con un nickname numerico'''
        attr:dict = {
            "nickname": 9876543210,
            "id": 9876543210
        }
        seller = Seller(**attr)
        seller.save()
        self.assertNotEqual(attr,SellerSerializer(Seller.objects.get(id=attr['id'])).data)
        attr['nickname'] = str(attr['nickname'])
        self.assertEqual(attr,SellerSerializer(Seller.objects.get(id=attr['id'])).data)
    #enddef

    def test_serialize_one_item(self):
        '''Test Serialize one Item'''        
        Item(**self.attr_item).save()        
        self.attr_item['seller'] = self.seller.id 
        self.assertEqual(self.attr_item,ItemSerializer(Item.objects.get(id=attr_item['id'])).data)        
    #enddef

    def test_serialize_list_item(self):
        '''Test Serialize list of Items'''
        lst_attr_items = []
        for idx in range(1,10):
            it_attr_item = self.attr_item.copy()
            it_attr_item['id'] = it_attr_item['id'] + str(idx)
            it_attr_item['title'] = str(idx) + it_attr_item['title']
            Item(**it_attr_item).save()
            it_attr_item['seller'] = self.seller.id 
            lst_attr_items.append(it_attr_item)            
        #endfor
        ## serializacion de todos los registros creados
        self.assertEqual(lst_attr_items,ItemSerializer(Item.objects.all(),many=True).data) 
    #enddef

    def test_create_list_item(self):
        '''Test Crate list of Item'''
        lst_attr_items = []
        for idx in range(1,10):
            it_attr_item = self.attr_item.copy()
            it_attr_item['id'] = it_attr_item['id'] + str(idx)
            it_attr_item['title'] = str(idx) + it_attr_item['title']
            Item(**it_attr_item).save()
            self.assertTrue(Item.objects.filter(id=it_attr_item['id']).exists()) 
            it_attr_item['seller'] = self.seller.id
            self.assertEqual(it_attr_item,ItemSerializer(Item.objects.get(id=it_attr_item['id'])).data)            
            lst_attr_items.append(it_attr_item)
        #endfor
        ## serializacion de todos los registros creados
        self.assertEqual(lst_attr_items,ItemSerializer(Item.objects.all(),many=True).data) 
    #enddef

    def test_delete_one_item(self):
        '''Test delete one item'''
        Item(**self.attr_item).save()
        self.assertTrue(Item.objects.filter(id=self.attr_item['id']).exists())
        Item.objects.get(id=self.attr_item['id']).delete()
        self.assertFalse(Item.objects.filter(id=self.attr_item['id']).exists())        
    #enddef

    def test_delete_all_item(self):
        '''Test delete all register from table'''
        lst_attr_items = []
        for idx in range(1,10):
            it_attr_item = self.attr_item.copy()
            it_attr_item['id'] = it_attr_item['id'] + str(idx)
            it_attr_item['title'] = str(idx) + it_attr_item['title']
            Item(**it_attr_item).save()            
            it_attr_item['seller'] = self.seller.id            
            lst_attr_items.append(it_attr_item)
        #endfor
        ## serializacion de todos los registros creados
        self.assertEqual(lst_attr_items,ItemSerializer(Item.objects.all(),many=True).data)
        Item.objects.all().delete()
        self.assertEqual(len(Item.objects.all()),0)
    #enddef
#endclass


class TestModelItem_json2object(TestCase):
    def setUp(self):
        self.attr_json = attr_item_json
        self.attr = json.loads(attr_item_json)
        self.seller = Seller.json2object(self.attr['seller'])
        self.seller.save()        
    #endif

    def test_create_item(self):
        '''Test create Item'''
        item = Item.json2object(self.attr_json)
        item.save()
        self.assertTrue(Item.objects.filter(id=self.attr['id']).exists())
        self.attr['seller'] = self.seller.id
        self.assertEqual(self.attr,ItemSerializer(Item.objects.get(id=self.attr['id'])).data)
    #enddef

    def test_create_item_form_dict(self):
        '''Test create Item'''
        item = Item.json2object(json.loads(self.attr_json))
        item.save()
        self.assertTrue(Item.objects.filter(id=self.attr['id']).exists())
        self.attr['seller'] = self.seller.id
        self.assertEqual(self.attr,ItemSerializer(Item.objects.get(id=self.attr['id'])).data)
    #enddef

    def test_create_item_id_int(self):
        '''Test Create Item con id entero no str'''        
        self.attr['id'] = 9876543219876        
        Item.json2object(json.dumps(self.attr)).save()
        self.attr['seller'] = self.seller.id
        self.assertNotEqual(self.attr,ItemSerializer(Item.objects.get(id=str(self.attr['id']))).data)
        self.attr['id'] = str(self.attr['id'])
        self.assertEqual(self.attr,ItemSerializer(Item.objects.get(id=self.attr['id'])).data)
    #enddef

    def test_create_item_raise(self):        
        attr = []
        with self.assertRaises((ValueError,TypeError,utils.IntegrityError)):
            Item.json2object(attr).save()
        #endwith        
    #enddef

    def test_create_item_raise_without_seller(self):        
        self.attr['seller'] = {'id':12,'nickname':'none'}
        with self.assertRaises((ValueError,TypeError,utils.IntegrityError)):
            Item.json2object(json.dumps(self.attr)).save()
        #endwith        
    #enddef

    def test_create_item_raise_seller_None(self):        
        self.attr['seller'] = None
        with self.assertRaises((ValueError,TypeError,utils.IntegrityError)):
            Item.json2object(json.dumps(self.attr)).save()
        #endwith        
    #enddef

    def test_create_item_raise_seller_int(self):        
        self.attr['seller'] = 10
        with self.assertRaises((ValueError,TypeError,utils.IntegrityError)):
            Item.json2object(json.dumps(self.attr)).save()
        #endwith        
    #enddef

    def test_create_item_raise_seller_without_id(self):        
        self.attr['seller'] = {'fakeid':12,'nickname':'none'}        
        with self.assertRaises((ValueError,TypeError,utils.IntegrityError)):
            Item.json2object(json.dumps(self.attr)).save()
        #endwith        
    #enddef
    def test_create_seller_nickname_int(self):
        '''Creacion de un seller con un nickname numerico'''
        self.attr['seller'] = {'id':9876543210,'nickname':9876543210}
        seller = Seller.json2object(json.dumps(self.attr['seller']))
        seller.save()
        Item.json2object(json.dumps(self.attr)).save()
        self.attr['seller'] = seller.id
        self.assertEqual(self.attr,ItemSerializer(Item.objects.get(id=self.attr['id'])).data)        
    #enddef
#endclass