'''
Docstring for rd_wepapp.items.tests_api_ItemsView_post

python3 manage.py test -v 2 items.tests_api_ItemsView_post
'''

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

data_post = {
    "title": "Titulo test Item",
    "price": 29449.50,    
    "id": "TEST-ITEM123456789",
    "thumbnail": "http://",
    "listing_type_id": "gold_special",
    "seller":{
        "nickname": "SellerTest",
        "id": 237004002253
    }
}

class TestView_ItemsView_WithoutRegister(TestCase):
    '''modelo para los test case relacionado ItemsView sin registros'''

    def setUp(self):
        '''inicializacion para cada metodo'''
        self.clien = Client()
        #response = self.clien.post(self.url,data_post,content_type='application/json')
        self.attr_post={'content_type':'application/json','path':"/api/items/"}
        self.url = "/api/items/"


    def test_items(self):
        '''Test response without items'''        
        response = self.clien.post(**self.attr_post,data=data_post)
        #print(f'response.content: {json.loads(response.content)}')
        self.assertEqual(response.status_code,404)


class TestView_ItemsView(TestCase):
    '''modelo para los test case relacionado ItemsView'''

    def setUp(self):
        '''inicializacion para cada metodo'''
        self.attr_post={'content_type':'application/json','path':"/api/items/"}
        self.url = "/api/items/"
        self.seller = Seller(**attr_seller)
        self.seller.save()
        self.attr_item = data_post.copy()
        self.attr_item['seller'] = self.seller.id

        self.client = Client()
        self.url = "/api/items/"

    def test_items(self):
        '''Test response without items'''
        response = self.client.post(**self.attr_post,data=data_post)
        #print(f'response.content: {response.content}')
        self.assertEqual(response.status_code,200)
        self.assertEqual(self.attr_item,
                        ItemSerializer(Item.objects.get(id=self.attr_item['id'])).data) # pylint: disable=no-member


    def test_items_TypeError_in_item(self):
        '''Test response without items'''        
        response = self.client.post(**self.attr_post,data=[data_post])
        #print(f'response.content: {response.content}')
        self.assertEqual(response.status_code,400)
        #self.assertEqual(self.attr_item,
        #       ItemSerializer(Item.objects.get(id=self.attr_item['id'])).data)

    def test_items_TypeError_in_seller(self):
        '''Test response without items'''        
        response = self.client.post(**self.attr_post,data=self.attr_item)
        #print(f'response.content: {response.content}')
        self.assertEqual(response.status_code,400)


#
#    def test_with_items(self):
#        '''Test response with items'''
#        lst_attr_items = []
#        for idx in range(1,10):
#            it_attr_item = self.attr_item.copy()
#            it_attr_item['id'] = it_attr_item['id'] + str(idx)
#            it_attr_item['title'] = str(idx) + it_attr_item['title']
#            Item(**it_attr_item).save()
#            it_attr_item['seller'] = self.seller.id
#            lst_attr_items.append(it_attr_item)
#        #endfor
#        self.assertEqual(lst_attr_items,ItemSerializer(Item.objects.all(),many=True).data)
#        response = self.clien.get(self.url)
#        self.assertEqual(json.loads(response.content),lst_attr_items)
#
