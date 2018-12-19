from django.test import TestCase
from django.urls import reverse
from psswdmng.models import *

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
		pass
		#User.objects.create(User_name = 'sys', Master_password_hash = b'123', Open_key = b'123')
		#User.objects.create(User_name = 'user1', Master_password_hash = b'123', Open_key = b'123')
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