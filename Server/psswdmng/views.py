from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
import datetime
import os
import string
import random

import cryptography
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


# Create your views here.

def index(request):
	return HttpResponse("You're in start page")

def get_password(request):
	if authentificate(request.GET.getlist('auth_seq'), username = request.GET['user']) != 0:
		return HttpResponse('Authentification error!')
	else:
		user_obj = User.objects.get(User_name = request.GET['user'])
		user_obj.Authentication_sequence = None
		user_obj.save()
	url = request.GET['url']
	login = request.GET['login']
	result = Main_record.objects.get(pair_id = Pair.objects.get(login_id = Login.objects.get(Login = login), resource_id = Resource.objects.get(URL = url)), user_id = User.objects.get(User_name = request.GET['user']))
	return HttpResponse(result.Password)

@csrf_exempt	
def add_user(request):
	username = request.POST['username']
	passwordhash = request.POST['passwordhash']
	User.objects.create(User_name = username, Master_password_hash = passwordhash)
	return HttpResponse(0)
	
def authenticate(request):
	if authentificate(request.GET.getlist('auth_seq'), username = request.GET['user']) != 0:
		return HttpResponse('Authentification error!')
	else:
		user_obj = User.objects.get(User_name = request.GET['user'])
		user_obj.Authentication_sequence = None
		user_obj.save()
	#print(request.GET)
	username = request.GET['username']
	passwordhash = request.GET['passwordhash']
	user = User.objects.get(User_name = username)
	if str(user.Master_password_hash) == passwordhash:
		return HttpResponse(1)
	else:
		return HttpResponse(0)
		
@csrf_exempt
def add_password(request):
	if authentificate(request.POST.getlist('auth_seq'), username = request.POST['user']) != 0:
		return HttpResponse('Authentification error!')
	else:
		user_obj = User.objects.get(User_name = request.POST['user'])
		user_obj.Authentication_sequence = None
		user_obj.save()	
	no_pair = False
	url = request.POST['url']
	login = request.POST['login']
	password = request.POST['password']
	user = request.POST['user']
	pair = None
	if not Login.objects.filter(Login = login).exists():
		Login.objects.create(Login = login)
		no_pair = True
	if not Resource.objects.filter(URL = url).exists():
		Resource.objects.create(URL = url)
		no_pair = True
	if no_pair:
		pair = Pair.objects.create(login_id = Login.objects.get(Login = login), resource_id = Resource.objects.get(URL = url))
	elif not Pair.objects.filter(login_id = Login.objects.get(Login = login), resource_id = Resource.objects.get(URL = url)).exists():
		pair = Pair.objects.create(login_id = Login.objects.get(Login = login), resource_id = Resource.objects.get(URL = url))
	else:
		pair = Pair.objects.get(login_id = Login.objects.get(Login = login), resource_id = Resource.objects.get(URL = url))
	Main_record.objects.create(pair_id = pair, Password = password, user_id = User.objects.get(User_name = user), Change_date = datetime.datetime.now())
	return HttpResponse(0)
	
def get_authentication_sequence(request):
	username = request.GET['user']
	user = User.objects.get(User_name = username)
	open_key_bytes = user.Open_key
	public_key = load_pem_public_key(open_key_bytes, backend = default_backend())
	auth_seq = os.urandom(64)
	user.Authentication_sequence = auth_seq
	user.save()
	enc_auth_seq = public_key.encrypt(auth_seq, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
	return HttpResponse(enc_auth_seq, """content_type = 'application/octet-stream'""")
	
def authentificate(auth_seq, username):
	auth_bytes = b''
	for ch in auth_seq:
		auth_bytes += int(ch).to_bytes(1, byteorder = 'little', signed = False)
	if User.objects.get(User_name = username).Authentication_sequence != auth_bytes:
		return 1
	else:
		return 0

@csrf_exempt		
def change_password(request):
	if authentificate(request.POST.getlist('auth_seq'), username = request.POST['user']) != 0:
		return HttpResponse('Authentification error!')
	else:
		user_obj = User.objects.get(User_name = request.POST['user'])
		user_obj.Authentication_sequence = None
		user_obj.save()
	url = request.POST['url']
	login = request.POST['login']
	rec = Main_record.objects.get(pair_id = Pair.objects.get(login_id = Login.objects.get(Login = login), resource_id = Resource.objects.get(URL = url)), user_id = User.objects.get(User_name = request.POST['user']))
	rec.Password = request.POST['password']
	rec.Change_date = datetime.datetime.now()
	rec.save()
	return HttpResponse(0)
	