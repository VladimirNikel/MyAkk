from django.test import TestCase
from django.urls import reverse
from psswdmng.models import *
import datetime

#Create your tests here.

class ViewsTest(TestCase):
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

		#add user for test
		Login.objects.create(Login = 'somelogin')
		_login = Login.objects.get(Login = 'somelogin')
		Resource.objects.create(URL = 'someurl')
		_resource = Resource.objects.get(URL = 'someurl')
		Pair.objects.create(login_id = _login, resource_id = _resource)
		_pair = Pair.objects.get(login_id = _login, resource_id = _resource)
		User.objects.create(User_name = 'user1', Master_password_hash = b'123', Open_key = b'123', Session_started = True, Authentication_sequence = b'\x03\x02\x01')
		_user = User.objects.get(User_name = 'user1')
		Main_record.objects.create(pair_id = _pair, Password = 'oldpass', Change_date = datetime.datetime.now(), user_id = _user)		
		seq = [3, 2, 1]

		#test req method GET
		#response = self.client.get(url)
		#self.assertEqual(response.status_code, 200)
		#self.assertEqual(response.content, b"GET method is required! Send \'auth_seq\', \'username\', \'url\' and \'login\'")
		
		#test req method GET with null data
		test_data0 = {}
		#response = self.client.get(url, test_data0)
		#self.assertEqual(response.status_code, 200)
		#self.assertEqual(response.content, b"GET method is required! Send \'auth_seq\', \'username\', \'url\' and \'login\'")
		
		#test get_password with wrong data
		test_data1 = {'auth_seq': [3, 2, 1, 1], 'username': 'user1', 'url': 'someurl', 'login': 'somelogin'}
		response = self.client.get(url, test_data1)
		self.assertEqual(response.content, b"Authentification error!")

		#test get_password with right data
		test_data2 = {'auth_seq': seq, 'username': 'user1', 'url': 'someurl', 'login': 'somelogin'}
		response = self.client.get(url, test_data2)
		self.assertEqual(response.content, b"oldpass")
#3-------------------------------------------------------------------------------------------------------
	def test_add_user(self):
		pass
#4-------------------------------------------------------------------------------------------------------
	def test_authenticate(self):
		pass
#5-------------------------------------------------------------------------------------------------------
	def test_add_password(self):
		pass
#6-------------------------------------------------------------------------------------------------------
	def test_get_authentication_sequence(self):
		pass
#7-------------------------------------------------------------------------------------------------------
	def test_authentificate(self):
		pass
#8-------------------------------------------------------------------------------------------------------
	def test_change_password(self):
		pass
#9-------------------------------------------------------------------------------------------------------
	def test_start_session(self):
		pass
#10------------------------------------------------------------------------------------------------------
	def test_end_session(self):
		pass