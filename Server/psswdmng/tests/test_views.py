from django.test import TestCase
from django.urls import reverse
from psswdmng.models import *
from psswdmng.views import authentificate

import cryptography
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import datetime

#Create your tests here.
private_key = rsa.generate_private_key(public_exponent = 65537, key_size = 2048, backend = default_backend())

class ViewsTest(TestCase):
	@classmethod
	def setUpTestData(cls):
		#add user for test
		Login.objects.create(Login = 'somelogin')
		_login = Login.objects.get(Login = 'somelogin')

		Resource.objects.create(URL = 'someurl')
		_resource = Resource.objects.get(URL = 'someurl')

		Pair.objects.create(login_id = _login, resource_id = _resource)
		_pair = Pair.objects.get(login_id = _login, resource_id = _resource)

		User.objects.create(User_name = 'sys', Master_password_hash = b'123', Session_started = False)
		_user = User.objects.get(User_name = 'sys')
		Main_record.objects.create(pair_id = _pair, Password = 'oldpass', Change_date = datetime.datetime.now(), user_id = _user)
#0-------------------------------------------------------------------------------------------------------
	def setUp(self):
		_user = User.objects.get(User_name = 'sys')
		_user.Master_password_hash = b'123'
		_user.Authentication_sequence = b'\x03\x02\x01'
		_user.Session_started = False
		open_key = private_key.public_key()
		open_key_bytes = open_key.public_bytes(encoding = serialization.Encoding.PEM, format = serialization.PublicFormat.SubjectPublicKeyInfo)
		_user.Open_key = open_key_bytes
		_user.save()
		
		_login = Login.objects.get(Login = 'somelogin')
		_resource = Resource.objects.get(URL = 'someurl')
		_pair = Pair.objects.get(login_id = _login, resource_id = _resource)
		_main_record = Main_record.objects.get(pair_id = _pair, user_id = _user)
		_main_record.Password = 'oldpass'
		_main_record.save()
#1-------------------------------------------------------------------------------------------------------
	def test_index(self):
		url = reverse('index')

		#test req method GET
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.content, b"You're in start page")
		
		#test req method POST
		response = self.client.post(url, {})
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.content, b"You're in start page")
#2-------------------------------------------------------------------------------------------------------
	def test_get_password(self):
		url = reverse('get_password')
	
		#test req method GET
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.content, b"GET method is required! Send \'auth_seq\', \'username\', \'url\' and \'login\'")
		
		#test req method POST
		response = self.client.post(url)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.content, b"GET method is required! Send \'auth_seq\', \'username\', \'url\' and \'login\'")

		#test req method GET with null data
		test_data0 = {}
		response = self.client.get(url, test_data0)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.content, b"GET method is required! Send \'auth_seq\', \'username\', \'url\' and \'login\'")
		
		#test get_password with wrong data
		test_data1 = {'auth_seq': [3, 2, 1, 1], 'username': 'sys', 'url': 'someurl', 'login': 'somelogin'}
		response = self.client.get(url, test_data1)
		self.assertEqual(response.content, b"Authentification error!")

		#test get_password with right data and ended session
		test_data2 = {'auth_seq': ['3', '2', '1'], 'username': 'sys', 'url': 'someurl', 'login': 'somelogin'}
		response = self.client.get(url, test_data2)
		self.assertEqual(response.content, b"Your session has already ended")

		#test get_password with right data and started session
		_user = User.objects.get(User_name = 'sys')
		_user.Session_started = True
		_user.Authentication_sequence = b'\x03\x02\x01'
		_user.save()
		test_data2 = {'auth_seq': ['3', '2', '1'], 'username': 'sys', 'url': 'someurl', 'login': 'somelogin'}
		response = self.client.get(url, test_data2)
		self.assertEqual(response.content, b"oldpass")
#3-------------------------------------------------------------------------------------------------------
	def test_add_user(self):
		url = reverse('add_user')

		#gen open key for new user
		open_key = private_key.public_key()
		open_key_bytes = open_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)
		open_key_nums = []
		for i in open_key_bytes:
			open_key_nums.append(i)

		#test req method GET
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.content, b"POST method is required! Send \'username\' and \'passwordhash\'")
		
		#test req method POST
		response = self.client.post(url)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.content, b"POST method is required! Send \'username\' and \'passwordhash\'")

		#test req method POST with null data
		test_data0 = {}
		response = self.client.post(url, test_data0)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.content, b"POST method is required! Send \'username\' and \'passwordhash\'")
		
		#test add_user with wrong data
		test_data1 = {'auth_seq': [3, 2, 1, 1], 'user': 'sys', 'username': 'user1', 'passwordhash': b'123', 'openkey': open_key_nums}
		response = self.client.post(url, test_data1)
		self.assertEqual(response.content, b"Authentification error!")

		#test add_user with right data and ended session
		test_data2 = {'auth_seq': [3, 2, 1], 'user': 'sys', 'username': 'user1', 'passwordhash': b'123', 'openkey': open_key_nums}
		response = self.client.post(url, test_data2)
		self.assertEqual(response.content, b"Your session has already ended")

		#test add_user with right data and started session
		_user = User.objects.get(User_name = 'sys')
		_user.Session_started = True
		_user.Authentication_sequence = b'\x03\x02\x01'
		_user.save()
		test_data2 = {'auth_seq': [3, 2, 1], 'user': 'sys', 'username': 'user1', 'passwordhash': b'123', 'openkey': open_key_nums}
		response = self.client.post(url, test_data2)
		self.assertEqual(response.content, b"User was added!")

		#test add_user with right data and started session AGAIN
		_user = User.objects.get(User_name = 'sys')
		_user.Session_started = True
		_user.Authentication_sequence = b'\x03\x02\x01'
		_user.save()
		test_data2 = {'auth_seq': [3, 2, 1], 'user': 'sys', 'username': 'user1', 'passwordhash': b'123', 'openkey': open_key_nums}
		response = self.client.post(url, test_data2)
		self.assertEqual(response.content, b"This user is already exist!")
#4-------------------------------------------------------------------------------------------------------
	def test_authenticate(self):
		url = reverse('authenticate')

		#test req method GET
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.content, b"GET method is required! Send \'auth_seq\', \'username\' and \'passwordhash\'")
		
		#test req method POST
		response = self.client.post(url)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.content, b"GET method is required! Send \'auth_seq\', \'username\' and \'passwordhash\'")

		#test req method GET with null data
		test_data0 = {}
		response = self.client.get(url, test_data0)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.content, b"GET method is required! Send \'auth_seq\', \'username\' and \'passwordhash\'")
		
		#test authenticate with wrong data
		test_data1 = {'auth_seq': [3, 2, 1, 1], 'username': 'sys', 'passwordhash': b'123'}
		response = self.client.get(url, test_data1)
		self.assertEqual(response.content, b"Authentification error!")

		#test authenticate with right data and ended session
		test_data2 = {'auth_seq': [3, 2, 1], 'username': 'sys', 'passwordhash': b'123'}
		response = self.client.get(url, test_data2)
		self.assertEqual(response.content, b"Your session has already ended")

		#test authenticate with wrong pass and started session
		_user = User.objects.get(User_name = 'sys')
		_user.Session_started = True
		_user.Authentication_sequence = b'\x03\x02\x01'
		_user.save()
		test_data2 = {'auth_seq': [3, 2, 1], 'username': 'sys', 'passwordhash': b'1234'}
		response = self.client.get(url, test_data2)
		self.assertEqual(response.content, b"0")

		#test authenticate with right data and started session
		_user = User.objects.get(User_name = 'sys')
		_user.Session_started = True
		_user.Authentication_sequence = b'\x03\x02\x01'
		_user.save()
		test_data2 = {'auth_seq': [3, 2, 1], 'username': 'sys', 'passwordhash': b'123'}
		response = self.client.get(url, test_data2)
		self.assertEqual(response.content, b"1")
#5-------------------------------------------------------------------------------------------------------
	def test_add_password(self):
		url = reverse('add_password')

		#test req method GET
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.content, b"POST method is required! Send \'auth_seq\', \'username\', \'url\', \'login\', \'password\'")
		
		#test req method POST
		response = self.client.post(url)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.content, b"POST method is required! Send \'auth_seq\', \'username\', \'url\', \'login\', \'password\'")

		#test req method POST with null data
		test_data0 = {}
		response = self.client.post(url, test_data0)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.content, b"POST method is required! Send \'auth_seq\', \'username\', \'url\', \'login\', \'password\'")
		
		#test add_password with wrong data
		test_data1 = {'auth_seq': [3, 2, 1, 1], 'username': 'sys', 'url': 'someurl', 'login': 'somelogin', 'password': 'somepasswod'}
		response = self.client.post(url, test_data1)
		self.assertEqual(response.content, b"Authentification error!")

		#test add_password with right data and ended session
		test_data2 = {'auth_seq': [3, 2, 1], 'username': 'sys', 'url': 'someurl', 'login': 'somelogin', 'password': 'somepasswod'}
		response = self.client.post(url, test_data2)
		self.assertEqual(response.content, b"Your session has already ended")

		#test add_password with wrong data and started session
		_user = User.objects.get(User_name = 'sys')
		_user.Session_started = True
		_user.Authentication_sequence = b'\x03\x02\x01'
		_user.save()
		test_data2 = {'auth_seq': [3, 2, 1], 'username': 'sys', 'url': 'someurl', 'login': 'somelogin', 'password': 'somepasswod'}
		response = self.client.post(url, test_data2)
		self.assertEqual(response.content, b"This is already exist!")

		#test add_password with new url and started session
		_user = User.objects.get(User_name = 'sys')
		_user.Session_started = True
		_user.Authentication_sequence = b'\x03\x02\x01'
		_user.save()
		test_data2 = {'auth_seq': [3, 2, 1], 'username': 'sys', 'url': 'someurl1', 'login': 'somelogin', 'password': 'somepasswod'}
		response = self.client.post(url, test_data2)
		self.assertEqual(response.content, b"0")

		#test add_password with new login and started session
		_user = User.objects.get(User_name = 'sys')
		_user.Session_started = True
		_user.Authentication_sequence = b'\x03\x02\x01'
		_user.save()
		test_data2 = {'auth_seq': [3, 2, 1], 'username': 'sys', 'url': 'someurl1', 'login': 'somelogin1', 'password': 'somepasswod'}
		response = self.client.post(url, test_data2)
		self.assertEqual(response.content, b"0")

		#test add_password with new url, new login and started session
		_user = User.objects.get(User_name = 'sys')
		_user.Session_started = True
		_user.Authentication_sequence = b'\x03\x02\x01'
		_user.save()
		test_data2 = {'auth_seq': [3, 2, 1], 'username': 'sys', 'url': 'someurl2', 'login': 'somelogin2', 'password': 'somepasswod'}
		response = self.client.post(url, test_data2)
		self.assertEqual(response.content, b"0")
#6-------------------------------------------------------------------------------------------------------NEED_SOME_FIX_MAZAFAKA
	def test_get_authentication_sequence(self):
		url = reverse('get_authentication_sequence')
	
		#test req method GET
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.content, b"GET method is required! Send \'username\'")
		
		#test req method POST
		response = self.client.post(url)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.content, b"GET method is required! Send \'username\'")

		#test req method GET with null data
		test_data0 = {}
		response = self.client.get(url, test_data0)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.content, b"GET method is required! Send \'username\'")
		
		#test get_password with wrong data
		test_data1 = {'username': 'sysa'}
		response = self.client.get(url, test_data1)
		self.assertEqual(response.content, b"GET method is required! Send \'username\'")

		#test get_password with right data and NONE Authentication_sequence_ne_pashet_blet
		#_user = User.objects.get(User_name = 'sys')
		#_user.Authentication_sequence = None
		#_user.save()
		#test_data2 = {'username': 'sys'}
		#response = self.client.get(url, test_data2)
		#_user = User.objects.get(User_name = 'sys')
		#open_key_bytes = bytes(_user.Open_key)
		#public_key = load_pem_public_key(open_key_bytes, backend = default_backend())
		#auth_seq = _user.Authentication_sequence
		#_seq = public_key.encrypt(auth_seq, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
		#self.assertEqual(response.content, _seq)

		#test get_password with right data and curr Authentication_sequence
		#_user = User.objects.get(User_name = 'sys')
		#_user.Authentication_sequence = b'\x03\x02\x01'
		#_user.save()
		#test_data3 = {'username': 'sys'}
		#response = self.client.get(url, test_data3)
		#self.assertEqual(response.content, b"123")
#7-------------------------------------------------------------------------------------------------------
	def test_authentificate(self):
		self.assertEqual(authentificate([3, 2, 1], 'sys'), 0)
		self.assertEqual(authentificate([3, 2, 1, 1], 'sys'), 1)
#8-------------------------------------------------------------------------------------------------------
	def test_change_password(self):
		url = reverse('change_password')

		#test req method GET
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.content, b"POST method is required! Send \'auth_seq\', \'username\', \'url\', \'login\', \'password\'")
		
		#test req method POST
		response = self.client.post(url)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.content, b"POST method is required! Send \'auth_seq\', \'username\', \'url\', \'login\', \'password\'")

		#test req method POST with null data
		test_data0 = {}
		response = self.client.post(url, test_data0)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.content, b"POST method is required! Send \'auth_seq\', \'username\', \'url\', \'login\', \'password\'")
		
		#test add_password with wrong data
		test_data1 = {'auth_seq': [3, 2, 1, 1], 'username': 'sys', 'url': 'someurl', 'login': 'somelogin', 'password': 'somepasswod'}
		response = self.client.post(url, test_data1)
		self.assertEqual(response.content, b"Authentification error!")

		#test add_password with right data and ended session
		test_data2 = {'auth_seq': [3, 2, 1], 'username': 'sys', 'url': 'someurl', 'login': 'somelogin', 'password': 'somepasswod'}
		response = self.client.post(url, test_data2)
		self.assertEqual(response.content, b"Your session has already ended")

		#test add_password with right data and started session
		_user = User.objects.get(User_name = 'sys')
		_user.Session_started = True
		_user.Authentication_sequence = b'\x03\x02\x01'
		_user.save()
		test_data2 = {'auth_seq': [3, 2, 1], 'username': 'sys', 'url': 'someurl', 'login': 'somelogin', 'password': 'somepasswod'}
		response = self.client.post(url, test_data2)
		self.assertEqual(response.content, b"0")
#9-------------------------------------------------------------------------------------------------------
	def test_start_session(self):
		url = reverse('start_session')

		#gen open key for new user
		open_key = private_key.public_key()
		open_key_bytes = open_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)
		open_key_nums = []
		for i in open_key_bytes:
			open_key_nums.append(i)

		#test req method GET
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.content, b"POST method is required! Send \'auth_seq\', \'username\', \'openkey\'")
		
		#test req method POST
		response = self.client.post(url)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.content, b"POST method is required! Send \'auth_seq\', \'username\', \'openkey\'")

		#test req method POST with null data
		test_data0 = {}
		response = self.client.post(url, test_data0)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.content, b"POST method is required! Send \'auth_seq\', \'username\', \'openkey\'")
		
		#test start_session with wrong data
		test_data1 = {'auth_seq': [3, 2, 1, 1], 'username': 'sys', 'openkey': open_key_nums}
		response = self.client.post(url, test_data1)
		self.assertEqual(response.content, b"Authentification error!")

		#test start_session with eneded session
		test_data2 = {'auth_seq': [3, 2, 1], 'username': 'sys', 'openkey': open_key_nums}
		response = self.client.post(url, test_data2)
		self.assertEqual(response.content, b"Session started")

		#test start_session with started session
		_user = User.objects.get(User_name = 'sys')
		_user.Session_started = True
		_user.Authentication_sequence = b'\x03\x02\x01'
		_user.save()
		test_data2 = {'auth_seq': [3, 2, 1], 'username': 'sys', 'openkey': open_key_nums}
		response = self.client.post(url, test_data2)
		self.assertEqual(response.content, b"Your session has already started")
#10------------------------------------------------------------------------------------------------------
	def test_end_session(self):
		url = reverse('end_session')

		#test req method GET
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.content, b"POST method is required! Send \'auth_seq\', \'username\'")
		
		#test req method POST
		response = self.client.post(url)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.content, b"POST method is required! Send \'auth_seq\', \'username\'")

		#test req method POST with null data
		test_data0 = {}
		response = self.client.post(url, test_data0)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.content, b"POST method is required! Send \'auth_seq\', \'username\'")
		
		#test end_session with wrong data
		test_data1 = {'auth_seq': [3, 2, 1, 1], 'username': 'sys'}
		response = self.client.post(url, test_data1)
		self.assertEqual(response.content, b"Authentification error!")

		#test end_session with started session
		_user = User.objects.get(User_name = 'sys')
		_user.Session_started = True
		_user.save()
		test_data2 = {'auth_seq': [3, 2, 1], 'username': 'sys'}
		response = self.client.post(url, test_data2)
		self.assertEqual(response.content, b"Session ended")

		#test end_session with eneded session
		_user = User.objects.get(User_name = 'sys')
		_user.Session_started = False
		_user.Authentication_sequence = b'\x03\x02\x01'
		_user.save()
		test_data2 = {'auth_seq': [3, 2, 1], 'username': 'sys'}
		response = self.client.post(url, test_data2)
		self.assertEqual(response.content, b"Your session has already ended")