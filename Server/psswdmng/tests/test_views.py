from django.test import TestCase
from django.urls import reverse
from psswdmng.models import *

#Create your tests here.

class ViewsTest(TestCase):
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

    #---------------------------------------------------------------
    def test_add_user(self):
        url = reverse('add_user')

        #test req method GET
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"POST method is required! Send \'username\' and \'passwordhash\'")

        #test req method POST with null data
        test_data0 = {}
        response = self.client.post(url, test_data0)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"POST method is required! Send \'username\' and \'passwordhash\'")

        #test add user
        test_data1 = {'user': 'user1', 'passwordhash': '1111'}
        response = self.client.post(url, test_data1)
        #self.assertEqual(response.content, b"User was added!")

        #test add exist user
        response = self.client.post(url, test_data1)
        #self.assertEqual(response.content, b"This user is already exist!")
 
    #---------------------------------------------------------------authentificate(request.GET.getlist('auth_seq'), username = request.GET['username']) != 0:
    def test_authenticate(self):
        url = reverse('authenticate')

        #test req method GET
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"GET method is required! Send \'auth_seq\', \'username\' and \'passwordhash\'")

        #test req method POST with null data
        test_data0 = {}
        response = self.client.post(url, test_data0)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"GET method is required! Send \'auth_seq\', \'username\' and \'passwordhash\'")

        #test authenticate with wrong data
        test_data1 = {'auth_seq': '123', 'username': 'someusername', 'passwordhash': '123'}
        response = self.client.get(url, test_data1)
        self.assertEqual(response.content, b"Authentification error!")

        #create temp_user
        auth_seq = ['1', '2', '3']
        auth_bytes = b''
        for ch in auth_seq:
            auth_bytes += int(ch).to_bytes(1, byteorder = 'little', signed = False)      
        User.objects.create(User_name = 'user1', Master_password_hash = b'123', Authentication_sequence = auth_bytes)
        self.assertEqual(User.objects.get(User_name = 'user1').Authentication_sequence, auth_bytes)

        #test authenticate with wrong pass
        test_data1 = {'auth_seq': auth_seq, 'username': 'user1', 'passwordhash': '321'}
        response = self.client.get(url, test_data1)
        self.assertEqual(response.content, b"0")

        #test authenticate
        #test_data2 = {'auth_seq': auth_seq, 'username': 'user1', 'passwordhash': '123'}
        #response = self.client.get(url, test_data2)
        #self.assertEqual(response.content, b"1")

    #---------------------------------------------------------------
    def test_get_password(self):
        url = reverse('get_password')

        #test req method GET
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"GET method is required! Send \'auth_seq\', \'username\', \'url\' and \'login\'")

        #test req method POST with null data
        test_data0 = {}
        response = self.client.post(url, test_data0)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"GET method is required! Send \'auth_seq\', \'username\', \'url\' and \'login\'")
	
        #test get_password with wrong data
        test_data1 = {'auth_seq': '123', 'username': 'user1', 'url': 'someurl', 'login': 'somelogin'}
        response = self.client.get(url, test_data1)
        self.assertEqual(response.content, b"Authentification error!")

        #test get_password
        test_data2 = {'auth_seq': '123', 'username': 'someusername', 'url': 'someurl', 'login': 'somelogin'}
        response = self.client.get(url, test_data2)
        #self.assertEqual(response.content, b"0")
	
    #---------------------------------------------------------------
    def test_add_password(self):
        url = reverse('add_password')

        #test req method GET
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"POST method is required! Send \'auth_seq\', \'username\', \'url\', \'login\', \'password\'")

        #test req method POST with null data
        test_data0 = {}
        response = self.client.post(url, test_data0)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"POST method is required! Send \'auth_seq\', \'username\', \'url\', \'login\', \'password\'")

        #test add_password with wrong data
        test_data1 = {'auth_seq': '123', 'username': 'someusername', 'url': 'someurl', 'login': 'somelogin', 'password' : 'somepassword'}
        response = self.client.post(url, test_data1)
        self.assertEqual(response.content, b"Authentification error!")

        #test add_password/nsf
        #test_data2 = {'auth_seq': '123', 'username': 'someusername', 'url': 'someurl', 'login': 'somelogin', 'password' : 'somepassword'}
        #response = self.client.post(url, test_data2)
        #self.assertEqual(response.content, b"0")

    #---------------------------------------------------------------
    def test_get_authentication_sequence(self):
        url = reverse('get_authentication_sequence')

        #test req method GET
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"GET method is required! Send \'username\'")

        #test req method POST with null data
        test_data0 = {}
        response = self.client.post(url, test_data0)
        self.assertEqual(response.status_code, 200)
        #self.assertEqual(response.content, b"GET method is required! Send \'username\'")

        #test authentication_sequence with wrong data
        test_data1 = {'username': 'someusername'}
        response = self.client.get(url, test_data1)
        #self.assertEqual(response.content, b"This user doesn\'t exist!")

        #test authentication_sequence
        #test_data2 = {'username': 'someusername'}
        #response = self.client.get(url, test_data2)
        #self.assertEqual(response.content, b"0")

    #---------------------------------------------------------------
    def test_authentificate(self):
        pass

    #---------------------------------------------------------------
    def test_change_password(self):
        url = reverse('change_password')

        #test req method GET
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"POST method is required! Send \'auth_seq\', \'username\', \'url\', \'login\', \'password\'")

        #test req method POST with null data
        test_data0 = {}
        response = self.client.post(url, test_data0)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"POST method is required! Send \'auth_seq\', \'username\', \'url\', \'login\', \'password\'")

        #test change_password with wrong data
        test_data1 = {'auth_seq': '123', 'username': 'someusername', 'url': 'someurl', 'login': 'somelogin', 'password' : 'somepassword'}
        response = self.client.post(url, test_data1)
        self.assertEqual(response.content, b"Authentification error!")

        #test change_password/nsf
        #test_data2 = {'auth_seq': '123', 'user': 'someusername', 'url': 'someurl', 'login': 'somelogin', 'password' : 'somepassword'}
        #response = self.client.post(url, test_data2)
        #self.assertEqual(response.content, b"0")
	
