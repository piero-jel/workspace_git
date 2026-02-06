'''
Docstring for rd_wepapp.items.tests_api_ItemsView_get

    python3 manage.py test -v 2 items.tests_api_ItemsView_get

'''
import json
from django.test import TestCase,Client # type: ignore pylint: disable=import-error
#from django.db import utils
from .models import Item,Seller
from .serializers import ItemSerializer#,SellerSerializer
#from .views import ItemsView



# Create your tests here.
attr_seller:dict = {
    "nickname": "SellerTest",
    "id": 237004002253
}

seller = Seller(**attr_seller)

attr_item:dict = {
    "title": "Titulo test Item",
    "price": 29449.50,    
    "id": "TEST-ITEM123456789",
    "thumbnail": "http://",
    "listing_type_id": "gold_special"
}


class TestView_ItemsView_WithoutRegister(TestCase):
    '''modelo para los test case relacionado ItemsView sin registros'''
    def setUp(self):
        '''inicializacion para cada metodo'''
        self.clien = Client()
        self.url = "/api/items/"

    def test_items(self):
        '''Test response without items'''        
        response = self.clien.get(self.url)
        self.assertEqual(response.status_code,404)

    def test_item_paginate(self):
        '''Test pagionado'''
        self.url = "/api/items/?offset={}&limit={}"
        response = self.client.get(self.url.format(50,50))
        self.assertEqual(response.status_code,404)



class TestView_ItemsView(TestCase):
    '''modelo para los test case relacionado ItemsView sin registros'''
    def setUp(self):
        '''inicializacion para cada metodo'''
        self.seller = Seller(**attr_seller)
        self.seller.save()
        attr_item['seller'] = self.seller
        self.attr_item = attr_item.copy()

        self.clien = Client()
        self.url = "/api/items/"

    def test_without_items(self):
        '''Test response without items'''        
        response = self.clien.get(self.url)
        self.assertEqual(response.status_code,404)

    def test_with_items(self):
        '''Test response with items'''
        lst_attr_items = []
        for idx in range(1,10):
            it_attr_item = self.attr_item.copy()
            it_attr_item['id'] = it_attr_item['id'] + str(idx)
            it_attr_item['title'] = str(idx) + it_attr_item['title']
            Item(**it_attr_item).save()
            it_attr_item['seller'] = self.seller.id
            lst_attr_items.append(it_attr_item)

        self.assertEqual(lst_attr_items,ItemSerializer(Item.objects.all(),many=True).data) # pylint: disable=no-member
        response = self.clien.get(self.url)
        self.assertEqual(json.loads(response.content),lst_attr_items)

class TestView_ItemsViewPaginate(TestCase):
    '''modelo para los test case relacionado ItemsView con paginacion'''

    def setUp(self):
        '''inicializacion para cada metodo'''
        self.seller = Seller(**attr_seller)
        self.seller.save()
        attr_item['seller'] = self.seller
        self.attr_item = attr_item.copy()
        self.lst_attr_items = []
        for idx in range(1,110):
            it_attr_item = self.attr_item.copy()
            it_attr_item['id'] = it_attr_item['id'] + str(idx)
            it_attr_item['title'] = str(idx) + it_attr_item['title']
            Item(**it_attr_item).save()
            it_attr_item['seller'] = self.seller.id
            self.lst_attr_items.append(it_attr_item)

        #self.assertEqual(self.lst_attr_items,ItemSerializer(Item.objects.all(),many=True).data)
        self.client = Client()
        self.url = "/api/items/?offset={}&limit={}"

    def test_paginate_items(self):
        '''Test paginate response'''        
        #"/api/items/?offset=10&limit=25"
        response = self.client.get(self.url.format(10,25))
        self.assertEqual(json.loads(response.content),self.lst_attr_items[10:35])
        self.assertNotEqual(json.loads(response.content),self.lst_attr_items[10:34])

        #response = self.client.get("/api/items/?offset=50&limit=50")
        response = self.client.get(self.url.format(50,50))
        self.assertEqual(json.loads(response.content),self.lst_attr_items[50:100])
        self.assertNotEqual(json.loads(response.content),self.lst_attr_items[51:100])

        response = self.client.get(self.url.format(200,25))
        self.assertEqual(json.loads(response.content),self.lst_attr_items[0:25])
        self.assertNotEqual(json.loads(response.content),self.lst_attr_items[-25:])

    def test_paginado_error_type(self):
        '''test para error en el paginado'''
        response = self.client.get(self.url.format('a',25))
        self.assertEqual(response.status_code,400)



# Contemplar los casos cuando no existe Seller
