'''
Docstring for rd_wepapp.items.tests_views
    python3 manage.py test -v 2 items.tests_views
'''
#import json
from django.test import TestCase,Client # type: ignore pylint: disable=import-error
from django.db import utils             # type: ignore pylint: disable=import-error
from .models import Item,Seller
#from .serializers import ItemSerializer,SellerSerializer
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




class TestView_index(TestCase):
    ''' 
        [url] ip:port/ ex: http://localhost:8080/
    '''
    def test_without_items(self):
        '''Test response without items'''
        c = Client()
        response = c.get("/")
        #print(f'response: {response} | {response.content}')
        self.assertEqual(response.status_code,200)



class TestView_items_without_seller(TestCase):
    ''' [url] ip:port/items/items ex: http://localhost:8080/items
    '''
    def test_without_items_and_seller(self):
        '''Test response without items'''
        c = Client()
        response = c.get("/items/")
        #print(f'response: {response} | {response.context}')
        self.assertEqual(response.status_code,404)


    def test_try_items_without_seller(self):
        '''Test creacion de item sin un seeler'''
        with self.assertRaises(utils.IntegrityError):
            Item(**attr_item).save()




class TestView_items(TestCase):
    ''' [url] ip:port/items/ ex: http://localhost:8080/items/
    '''
    def setUp(self):
        '''inicializacion para cada metodo'''
        self.seller = Seller(**attr_seller)
        self.seller.save()
        self.attr_item = attr_item.copy()
        self.attr_item['seller'] = self.seller

        self.cliet = Client()
        self.get_attr = {'path':'/items/'}

    def test_without_items(self):
        '''Test response without items'''
        response = self.client.get(**self.get_attr)
        #print(f'response: {response} | {response.context}')
        self.assertEqual(response.status_code,404)


    def test_with_items(self):
        '''Test response with items'''
        lst_attr_items = []
        for idx in range(1,50):
            it_attr_item = self.attr_item.copy()
            it_attr_item['id'] = it_attr_item['id'] + str(idx)
            it_attr_item['title'] = str(idx) + it_attr_item['title']
            Item(**it_attr_item).save()
            it_attr_item['seller'] = self.seller.id
            lst_attr_items.append(it_attr_item)

        c = Client()
        response = c.get("/items/")
        self.assertEqual(response.status_code,200)
        for it in ('titulo','list_item'):
            self.assertIn(it,response.context)

        self.assertTrue( len(response.context["titulo"])> 0)
        self.assertTrue( len(response.context["list_item"])> 0)

        #print(f'response: {response} | {response.content}')
        queryset = Item.objects.all().values('title','price','thumbnail').order_by('-price')[:20] # pylint: disable=no-member
        # print(f"list_item: {response.context['list_item']}")
        # print(f"queryset: {queryset}")
        self.assertEqual(list(response.context['list_item']),list(queryset))
        self.assertNotEqual(response.context['list_item'],queryset)
        self.assertEqual(response.context['titulo'],"Lista de los 20 items mas caros")
        self.assertEqual(len(response.context['list_item']),20)



class TestView_items_vs_seller_without_seller(TestCase):
    '''TestView_items_vs_seller_without_seller'''
    def setUp(self):
        '''inicializacion para cada metodo'''
        self.client = Client()
        self.attr_get = {'path':"/items_vs_seller/"}

    def test_without_items(self):
        '''Test response without items'''        
        response = self.client.get(**self.attr_get)
        self.assertEqual(response.status_code,404)
        self.assertIn('exception',response.context)


class TestView_items_vs_seller(TestCase):
    ''' [url] ip:port/items_vs_seller 'http://localhost:8080/items_vs_seller'
    '''
    def setUp(self):
        '''inicializacion para cada metodo'''
        self.seller = Seller(**attr_seller)
        self.seller.save()
        self.attr_item = attr_item.copy()
        self.attr_item['seller'] = self.seller
        self.client = Client()
        self.attr_get = {'path':"/items_vs_seller/"}

    def test_without_items(self):
        '''Test response without items'''        
        response = self.client.get(**self.attr_get)
        self.assertEqual(response.status_code,404)
        self.assertIn('exception',response.context)

    def test_with_items(self):
        '''Test response with items'''
        lst_attr_items = []
        for idx in range(1,50):
            it_attr_item = self.attr_item.copy()
            it_attr_item['id'] = it_attr_item['id'] + str(idx)
            it_attr_item['title'] = str(idx) + it_attr_item['title']
            Item(**it_attr_item).save()
            it_attr_item['seller'] = self.seller.id
            lst_attr_items.append(it_attr_item)

        c = Client()
        response = c.get("/items_vs_seller/")
        self.assertEqual(response.status_code,200)
        for it in ('titulo','table_head','table_rows','head_with'):
            #self.assertTrue( it in response.context,True)
            self.assertIn( it ,response.context)

        self.assertTrue( len(response.context["titulo"])> 0)
        self.assertTrue( len(response.context["table_head"])> 0)
        self.assertTrue( len(response.context["table_rows"])> 0)
        self.assertTrue( 0.0 < response.context["head_with"]< 100)
