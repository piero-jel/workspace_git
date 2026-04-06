""" Unit test module

    python3 manage.py test Login
"""
from django.test import TestCase
from Login.models import Empresa,User,Programador
from config.unittest import TestCaseLogger


class EmpresaTestCase(TestCase):
    """ Unit test module

    python3 manage.py test Login.tests.test_models.EmpresaTestCase
    """
    @classmethod
    def setUpClass(cls):
        cls.log = TestCaseLogger.set(cls.__name__,__file__)
        return super().setUpClass()
    
    def setUp(self):
        # Create initial data for each test method
        Empresa.objects.create(nombre="company1",
                               telefono1="+5421215487",
                               email="company1@email.com"
                            )
        
        Empresa.objects.create(nombre="company2",
                               telefono1="+5421215587",
                               email="company2@email.com"
                            )
        
        self.log:TestCaseLogger = TestCaseLogger.get(self)

    def test_get(self):
        """ Unit test module

        python3 manage.py test Login.tests.test_models.EmpresaTestCase.test_get
        """
        emp:Empresa = Empresa.objects.get(nombre='company1')
        self.log.info(f"emps: {emp.to_str()}")
        self.assertEqual(emp.get('email'),"company1@email.com")
        self.assertIsNone(emp.get('username'))

    def test_get_all(self):
        """ Unit test module

        python3 manage.py test Login.tests.test_models.EmpresaTestCase.test_get_all
        """
        emps:list[Empresa] = Empresa.objects.all()
        for idx,emp in enumerate(emps):
            self.log.debug(f"emps[{idx:02}] = {emp.to_str()}")
            self.assertIsNotNone(emp)
            self.assertIsInstance(emp.to_dict(),dict)

    def test_item_to_dict(self):
        """ Unit test module

        python3 manage.py test Login.tests.test_models.EmpresaTestCase.test_item_to_dict
        """
        emp:Empresa = Empresa.objects.get(nombre='company1')
        val = Empresa.item_to_dict(item=emp)
        self.assertIsInstance(val,dict)
        self.log.info(f"val: {val}")
        val2 = Empresa.item_to_dict()
        self.assertIsInstance(val2,dict)
        self.log.info(f"val2: {val2}")

    def test_to_dict(self):
        """ Unit test module

        python3 manage.py test Login.tests.test_models.EmpresaTestCase.test_to_dict
        """        
        emp:Empresa = Empresa.objects.get(nombre='company1')
        val = emp.to_dict()
        self.assertIsInstance(val,dict)
        self.log.info(f"val: {val}")
        

class UserTestCase(TestCase):
    """ Unit test module

    python3 manage.py test Login.tests.test_models.UserTestCase
    """
    @classmethod
    def setUpClass(cls):
        cls.log = TestCaseLogger.set(cls.__name__,__file__)
        return super().setUpClass()
    
    def setUp(self):
        # Create initial data for each test method
        User.objects.create(username="user1", first_name="User",last_name="Uno")
        User.objects.create(username="user2", first_name="user",last_name="Dos")
        self.log:TestCaseLogger = TestCaseLogger.get(self)

    def test_get(self):
        """
        python3 manage.py test Login.tests.test_models.UserTestCase.test_get
        """
        usr1:User = User.objects.get(username='user1')
        self.log.info(f"usr1: {usr1}")        
        self.assertEqual(usr1.get('username'),'user1')
        self.assertIsNone(usr1.get('name'))
    
    def test_item_to_dict(self):
        """
            python3 manage.py test Login.tests.test_models.UserTestCase.test_item_to_dict
        """
        usr2:User = User.objects.get(username='user1')
        val = User.item_to_dict(usr2)
        self.assertIsInstance(val,dict)
        self.log.info(f"val: {val}")
        val2 = User.item_to_dict()
        self.assertIsInstance(val2,dict)
        self.log.info(f"val2: {val2}")

    def test_to_dict(self):
        """
            python3 manage.py test Login.tests.test_models.UserTestCase.test_to_dict
        """
        usr2:User = User.objects.get(username='user1')
        val = usr2.to_dict()
        self.assertIsInstance(val,dict)
        self.log.info(f"val: {val}")
        


class ProgramadorTestCase(TestCase):
    """ Unit test module

    python3 manage.py test Login.tests.test_models.ProgramadorTestCase
    """
    @classmethod
    def setUpClass(cls):
        cls.log = TestCaseLogger.set(cls.__name__,__file__)
        return super().setUpClass()
    
    def setUp(self):
        # Create initial data for each test method
        User.objects.create(username="user1", first_name="User",last_name="Uno")        
        users:list[User] = [
            User.objects.create(username="programer1",
                        first_name="programador",last_name="Uno",
                        email='sysapp_programer1@email.com'
                    ),
            User.objects.create(username="programer2",
                        first_name="Programador2",last_name="dos",
                        email='sysapp_programer2@email.com'
                    )
        ]
        User.objects.create(username="user2", first_name="user",last_name="Dos")

        for usr in users:
            Programador.objects.create( programador=usr)

        self.log:TestCaseLogger = TestCaseLogger.get(self)

    def test_get(self):
        """ Unit test module

        python3 manage.py test Login.tests.test_models.ProgramadorTestCase.test_get
        """
        usr_id = User.objects.get(username='programer1')
        prg1:Programador = Programador.objects.get(programador=usr_id)
        self.log.info(f"prg1: {prg1} | {prg1.to_str()}")
        self.assertEqual(prg1.get('username'),'programer1')
        self.assertIsNone(prg1.get('name'))

    def test_item_to_dict(self):
        """ Unit test module

        python3 manage.py test Login.tests.test_models.ProgramadorTestCase.test_item_to_dict
        """
        usr_id = User.objects.get(username='programer1')
        usr1:Programador = Programador.objects.get(programador=usr_id)
        val = Programador.item_to_dict(item=usr1)
        self.assertIsInstance(val,dict)
        self.log.info(f"val: {val}")
        val2 = Programador.item_to_dict()
        self.assertIsInstance(val2,dict)
        self.log.info(f"val2: {val2}")

    def test_to_dict(self):
        """ Unit test module

        python3 manage.py test Login.tests.test_models.ProgramadorTestCase.test_to_dict
        """
        usr_id = User.objects.get(username='programer1')
        usr1:Programador = Programador.objects.get(programador=usr_id)
        val = usr1.to_dict()
        self.assertIsInstance(val,dict)
        self.log.info(f"val: {val}")

    def test_get_all(self):
        """ Unit test module

        python3 manage.py test Login.tests.test_models.ProgramadorTestCase.test_get_all
        """
        progs:list[Programador] = Programador.objects.all()
        for idx,emp in enumerate(progs):
            self.log.debug(f"progs[{idx:02}] = {emp.to_str()}")
            self.assertIsNotNone(emp)
            self.assertIsInstance(emp.to_dict(),dict)
        
        users:list[User] = User.objects.all()
        for idx,emp in enumerate(users):
            self.log.debug(f"user[{idx:02}] = {emp.to_str()}")
            self.assertIsNotNone(emp)
            self.assertIsInstance(emp.to_dict(),dict)