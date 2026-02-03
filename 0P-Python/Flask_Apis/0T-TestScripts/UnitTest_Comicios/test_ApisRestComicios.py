#!/usr/bin/env python3
''' Brief
  Modulo python para realizar test (no automatizados), Unitest para el test de Apis Rest

Llamado mediante
  python3 -m unittest test_Comicios.py
'''
from pathlib import Path
import json

import unittest   # import lib unit test
from Comicios import Comicio # import Object under test pylint: disable=import-error
from utils import get_log,Logger  #pylint: disable=import-error

class TestComicioApis(unittest.TestCase):
    '''
    Modelo para los test de la apis Comicio
    '''

    @classmethod
    def setUpClass(cls):
        # path file json, donde se realiza el load/store del objeto principal
        cls.json_file:str = 'ou/TestComicioApis.json'
        cls.log:Logger = get_log('TestComicioApis')

    def setUp(self):
        ''' Metodo set up, el cual se encarga de lebantar los datos almacenados 
        desde un archivo json.
        '''
        cls = type(self)
        if not Path(cls.json_file).exists():
            self.comicio =  Comicio(username='Usuario',password='pass1234',logger=cls.log)
            return super().setUp()

        content:str = ''
        with open(cls.json_file,"r",encoding='utf-8') as f2r:
            for it in f2r:
                tmp = it.rstrip()
                content += tmp.lstrip()

        # En caso de archivo vacio
        if content :
            self.comicio = Comicio(logger=cls.log,**json.loads(content))
        else:
            self.comicio = Comicio(username='Usuario',password='pass1234',logger=cls.log)

        return super().setUp()

    def tearDown(self):
        '''Metodo que se encarga de almacenar los datos en un archivo'''
        cls = type(self)
        with open(cls.json_file, 'w',encoding='utf-8') as f2w:
            json.dump(self.comicio.to_json(), f2w,indent=2)

        return super().tearDown()

    def test_create_user(self):
        '''01- test create user'''    
        target = 'create_user'
        params = {
            'url'  : self.comicio.get_endpoint(target) ,
            'json' : self.comicio.get_payload(target),
            'auth' : self.comicio.get_auth(target)
        }
        resp = self.comicio.request_method(target)(**params)
        self.assertTrue(self.comicio.verify_response(type=target,response=resp,repeat=True))

    def test_edit_user(self):
        '''02- test edit user'''    
        target = 'edit_user'
        params = {
            'url'  : self.comicio.get_endpoint(target),
            'json' : self.comicio.get_payload(target),
            'auth' : self.comicio.get_auth(target)
        }
        resp = self.comicio.request_method(target)(**params)
        self.assertTrue(self.comicio.verify_response(type=target,response=resp))

    def test_get_users(self):
        '''03- test get users'''    
        target = 'get_users'
        params = {
            'url'  : self.comicio.get_endpoint(target),
            'auth' : self.comicio.get_auth(target)
        }
        resp = self.comicio.request_method(target)(**params)
        self.assertTrue(self.comicio.verify_response(type=target,response=resp))

    def test_login(self):
        '''04- test login'''    
        target = 'login'
        params = {
            'url'  : self.comicio.get_endpoint(target),
            'auth' : self.comicio.get_auth(target)
        }
        resp = self.comicio.request_method(target)(**params)
        self.assertTrue(self.comicio.verify_response(type=target,response=resp))

    def test_health_check(self):
        '''05- test health check'''    
        target = 'health_check'
        params = {
            'url'  : self.comicio.get_endpoint(target),
            'auth' : self.comicio.get_auth(target)
        }
        resp = self.comicio.request_method(target)(**params)
        self.assertTrue(self.comicio.verify_response(type=target,response=resp))

    def test_post_comicio(self):
        '''06- test post comicio'''    
        target = 'comicio'
        path_file:str = 'in/post_comicio_01.json'
        params = {
            'url'  : self.comicio.get_endpoint(target),
            'json' : self.comicio.get_payload(target,path=path_file),
            'auth' : self.comicio.get_auth(target)
        }
        resp = self.comicio.request_method(target)(**params)
        self.assertTrue(self.comicio.verify_response(type=target,response=resp))

    def test_get_comicios(self):
        '''07- test get comicios'''    
        target = 'get_comicios'
        params = {
            'url'  : self.comicio.get_endpoint(target),
            'auth' : self.comicio.get_auth(target)
        }
        resp = self.comicio.request_method(target)(**params)
        self.assertTrue(self.comicio.verify_response(type=target,response=resp))

    def test_get_comicio_id(self):
        '''08- test get comicio id'''    
        target = 'get_comicio_id'
        params = {
            'url'  : self.comicio.get_endpoint(target,id=self.comicio.ids[0]),
            'auth' : self.comicio.get_auth(target)
        }
        resp = self.comicio.request_method(target)(**params)
        self.assertTrue(self.comicio.verify_response(type=target,response=resp))

    def test_get_comicio_id_list(self):
        '''09- test get comicio id desde la lista de get comicios'''    
        target = 'get_comicio_id'
        params = {
            'url'  : None,      
            'auth' : self.comicio.get_auth(target)
        }
        for it in self.comicio.ids:
            params['url'] = self.comicio.get_endpoint(target,id=it)
            resp = self.comicio.request_method(target)(**params)
            self.assertTrue(self.comicio.verify_response(type=target,response=resp))

    def test_post_comicio_list(self):
        '''10- test post comicio, desde una lista de archivos'''    
        target = 'comicio'
        path_file:str = 'in/post_comicio_{:02d}.json'
        params = {
        'url'  : self.comicio.get_endpoint(target) ,      
        'auth' : self.comicio.get_auth(target)
        }
        for idx in range(1,4):
            #params['json'] = self.comicio.get_payload(target,path=f'in/post_comicio_{idx:02}.json')
            params['json'] = self.comicio.get_payload(target,path=path_file.format(idx))
            resp = self.comicio.request_method(target)(**params)
            self.assertTrue(self.comicio.verify_response(type=target,response=resp))


def create_suite():
    '''Fucion que se encarga de armar la secuencia de llamado a cada test de forma 
    individual.
    '''
    tlp_test:tuple = [
        TestComicioApis('test_create_user'),
        TestComicioApis('test_edit_user'),
        TestComicioApis('test_get_users'),
        TestComicioApis('test_login'),
        TestComicioApis('test_health_check'),
        TestComicioApis('test_post_comicio'),
        TestComicioApis('test_get_comicios'),
        TestComicioApis('test_get_comicio_id'),
        TestComicioApis('test_get_comicio_id_list'),
        TestComicioApis('test_post_comicio_list'),
    ]

    return unittest.TestSuite(tests=tlp_test)


if __name__ == '__main__':
    suite = create_suite()
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
