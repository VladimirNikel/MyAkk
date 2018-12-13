"""
В данном файле описан набор функций-обработчиков http-запросов к серверу, а таке вспомогательных функций, необходимых для корректной работы сервера.
Все описанные аргументы функций-обработчиков http-запросов заключены в единственном, передаваемом каждой каждой функции, аргументе request, представляющем
собой словарь, где ключами являются названия аргументов.
"""

from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
import datetime
import os
import string
import random
from django.db import IntegrityError

import cryptography
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


## Обработчик http-запроса на получение стартовой страницы
def index(request):
	return HttpResponse("You're in start page")
	
	
## Обработчик http-запроса на выдачу пароля от ресурса
# 
# Тип запроса: \b GET
#
# Структура запроса: \c URL<b>/getpassword/</b>, где \c URL – ip-адрес и порт, на которых развёрнут сервер.
# \param auth_seq 	Список (массив) чисел, представляющий собой байты расшифрованной аутентификационной последовательности, выданной клиентскому приложению
# \param user 		Имя пользователя, от которого поступает запрос
# \param url		Адрес сайта, пароль к которому должен быть предоставлен
# \param login		Логин пользователя на сайте, к которому требуется предоставить пароль
# \returns 			<b>"Authentification error"</b>, если запрос не прошёл аутентификацию
# \returns 			<b>"Your session has already ended"</b>, если сессия пользователя уже была завершена
# \returns			<b>Password</b> – запрошенный пароль пользователя, если запрос прошёл успешно
# \returns			<b>Error message</b> – сообщение о непредвиденной ошибке с указаниями возможных действий пользователя по её устранению
def get_password(request):
		try:
			if authentificate(request.GET.getlist('auth_seq'), username = request.GET['username']) != 0:
				return HttpResponse("Authentification error!")
			else:
				user_obj = User.objects.get(User_name = request.GET['username'])
				user_obj.Authentication_sequence = None
				user_obj.save()
			user_obj = User.objects.get(User_name = request.POST['username'])
			if(user_obj.Session_started == False):
				return HttpResponse("Your session has already ended")
			url = request.GET['url']
			login = request.GET['login']
			result = Main_record.objects.get(pair_id = Pair.objects.get(login_id = Login.objects.get(Login = login), resource_id = Resource.objects.get(URL = url)), user_id = User.objects.get(User_name = request.GET['username']))
			return HttpResponse(result.Password)
		except:
			return HttpResponse("GET method is required! Send \'auth_seq\', \'username\', \'url\' and \'login\'")

	
## Обработчик http-запроса на добавление нового пользователя
#
# Тип запроса: \b POST
#
# Структура запроса: \c URL<b>/adduser/</b>, где \c URL – ip-адрес и порт, на которых развёрнут сервер.
# \param auth_seq 		Список (массив) чисел, представляющий собой байты расшифрованной аутентификационной последовательности, выданной клиентскому приложению
# \param user 			Имя пользователя, от которого поступает запрос (в данном случае – пользователь "Система")
# \param username 		Имя добавляемого пользователя 
# \param passwordhash 	Хэш пароля добавляемого пользователя
# \returns 				<b>"Authentification error"</b>, если запрос не прошёл аутентификацию
# \returns 				<b>"Your session has already ended"</b>, если сессия пользователя уже была завершена
# \returns				<b>Sucsess message</b> – сообщение об успешном добавлении пользователя, если пользователь добавлен успешно
# \returns				<b>User exists</b> – сообщение о существовании такого пользователя, если такое имя пользователя уже зарегистрировано в системе или является зарезервированным
# \returns				<b>Error message</b> – сообщение о непредвиденной ошибке с указаниями возможных действий пользователя по её устранению
# \note 				Допустимы только имена, под которыми ещё не были зарегистрированы пользователи в системе. Также запрещено имя \c sys, т.к. оно зарезервировано для нужд системы.
@csrf_exempt	
def add_user(request):
		try:
			if authentificate(request.POST.getlist('auth_seq'), username = request.POST['user']) != 0:
				return HttpResponse('Authentification error!')
			elif(request.POST['user'] != 'sys'):
				return HttpResponse('Authentification error!')
			else:
				user_obj = User.objects.get(User_name = request.POST['user'])
				user_obj.Authentication_sequence = None
				user_obj.save()
			user_obj = User.objects.get(User_name = request.POST['username'])
			if(user_obj.Session_started == False):
				return HttpResponse("Your session has already ended")
			open_key_array = request.POST.getlist('openkey')
			open_key = b''
			for ch in open_key_array:
				open_key += int(ch).to_bytes(1, byteorder = 'little', signed = False)
			passwordhash = request.POST['passwordhash']
			print(type(passwordhash))
			username = request.POST['username']
			User.objects.create(User_name = username, Master_password_hash = passwordhash, Open_key = open_key)
			return HttpResponse("User was added!")
		except IntegrityError:
			return HttpResponse("This user is already exist!")
		except:
			return HttpResponse("POST method is required! Send \'username\' and \'passwordhash\'")

				
## Обработчик http-запроса на аутентификацию пользователя, сделавшего попытку выполнить вход в систему с программы-клиента
#
# Тип запроса: \b GET
#
# Структура запроса: \c URL<b>/authenticate/</b>, где \c URL – ip-адрес и порт, на которых развёрнут сервер.
# \param auth_seq 		Список (массив) чисел, представляющий собой байты расшифрованной аутентификационной последовательности, выданной клиентскому приложению	
# \param user 			Имя пользователя, от которого поступает запрос
# \param username		Имя пользователя, которого необходимо аутентифицировать
# \param passwordhash	Хэш пароля пользователя, являющийся аутентификатором
# \returns 				<b>"Authentification error"</b>, если запрос не прошёл аутентификацию
# \returns 				<b>"Your session has already ended"</b>, если сессия пользователя уже была завершена
# \returns				\b 0, если пользователь успешно прошёл аутентификацию
# \returns				\b 1, аутентификация пользователя провалена
# \returns				<b>Error message</b> – сообщение о непредвиденной ошибке с указаниями возможных действий пользователя по её устранению
def authenticate(request):
		try:
			"""if authentificate(request.GET.getlist('auth_seq'), username = request.GET['username']) != 0:
				return HttpResponse("Authentification error!")
			else:
				user_obj = User.objects.get(User_name = request.GET['username'])
				user_obj.Authentication_sequence = None
				user_obj.save()
			user_obj = User.objects.get(User_name = request.POST['username'])
			if(user_obj.Session_started == False):
				return HttpResponse("Your session has already ended")"""
			username = request.GET['username']
			passwordhash = request.GET['passwordhash']
			user = User.objects.get(User_name = username)
			if str(user.Master_password_hash) == passwordhash:
				return HttpResponse(1)
			else:
				return HttpResponse(0)
		except:
			return HttpResponse("GET method is required! Send \'auth_seq\', \'username\' and \'passwordhash\'");


## Обработчик http-запроса на добавление основных данных (адрес ресурса, логин и пароль пользователя на ресурсе)
#
# Тип запроса: \b POST
#
# Структура запроса: \c URL<b>/addpassword/</b>, где \c URL – ip-адрес и порт, на которых развёрнут сервер.
# \param auth_seq 		Список (массив) чисел, представляющий собой байты расшифрованной аутентификационной последовательности, выданной клиентскому приложению
# \param user 			Имя пользователя, от которого поступает запрос
# \param url			URL-адрес ресурса, на котором осуществляется аутентификация с добавляемым паролем
# \param login			Логин пользователя, по которому осуществляется идентификация пользователя на ресурсе
# \param password		Добавляемый пароль, по которому будет осуществляться аутентификация пользователя на ресурсе
# \returns 				<b>"Authentification error"</b>, если запрос не прошёл аутентификацию
# \returns 				<b>"Your session has already ended"</b>, если сессия пользователя уже была завершена
# \returns				\b 0, если данные успешно дабавлены	
# \returns				<b>Error message</b> – сообщение о непредвиденной ошибке с указаниями возможных действий пользователя по её устранению
# \note 				Если данные, указанные в запросе, не существуют в базе (за исключением имени пользователя), они будут добавлены.				
@csrf_exempt
def add_password(request):
		try:
			if authentificate(request.POST.getlist('auth_seq'), username = request.POST['username']) != 0:
				return HttpResponse('Authentification error!')
			else:
				user_obj = User.objects.get(User_name = request.POST['username'])
				user_obj.Authentication_sequence = None
				user_obj.save()
			user_obj = User.objects.get(User_name = request.POST['username'])
			if(user_obj.Session_started == False):
				return HttpResponse("Your session has already ended")
			no_pair = False
			url = request.POST['url']
			login = request.POST['login']
			password = request.POST['password']
			user = request.POST['username']
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
		except:
			return HttpResponse("POST method is required! Send \'auth_seq\', \'username\', \'url\', \'login\', \'password\'");
		


## Обработчик http-запроса на добавление основных данных (адрес ресурса, логин и пароль пользователя на ресурсе)
#
# Тип запроса: \b GET
#
# Структура запроса: \c URL<b>/getauthseq/</b>, где \c URL – ip-адрес и порт, на которых развёрнут сервер.
# \param user 		Имя пользователя, от которого поступает запрос
# \returns 			\b enc_auth_seq – зашифрованная последовательность байт, передаваемая пользователю для аутентификации запроса
# \returns			<b>Error message</b> – сообщение о непредвиденной ошибке с указаниями возможных действий пользователя по её устранению		
def get_authentication_sequence(request):
		try:
			username = request.GET['username']
			user = User.objects.get(User_name = username)
			open_key_bytes = bytes(user.Open_key)
			public_key = load_pem_public_key(open_key_bytes, backend = default_backend())
			auth_seq = None
			if not user.Authentication_sequence
				auth_seq = os.urandom(64)
				user.Authentication_sequence = auth_seq
				user.save()
			else:
				auth_seq = user.Authentication_sequence
			enc_auth_seq = public_key.encrypt(auth_seq, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
			return HttpResponse(enc_auth_seq, content_type = 'application/octet-stream')
		except:
			return HttpResponse("GET method is required! Send \'username\'");


## Функция, выполняющая аутентификацию запроса	
# \param auth_seq	Аутентификационная последовательность, отправленная клиентской программой
# \param username	Имя пользователя, чей запрос необходимо аутентифицировать (отправителя последовательности)
# \returns 			\b 0, если запрос прошёл аутентификацию
# \returns 			\b 1, если запрос не прошёл аутентификацию
# \returns			\b -1,если возникла непредвиденная ошибка
def authentificate(auth_seq, username):
		try:
			auth_bytes = b''
			for ch in auth_seq:
				auth_bytes += int(ch).to_bytes(1, byteorder = 'little', signed = False)
			if bytes(User.objects.get(User_name = username).Authentication_sequence) != auth_bytes:
				return 1
			else:
				return 0
		except:
			return -1

		
## Обработчик http-запроса на замену пароля от ресурса
#
# Тип запроса: \b POST
#
# Структура запроса: \c URL<b>/changepassword/</b>, где \c URL – ip-адрес и порт, на которых развёрнут сервер.
# \param auth_seq 		Список (массив) чисел, представляющий собой байты расшифрованной аутентификационной последовательности, выданной клиентскому приложению
# \param user 			Имя пользователя, от которого поступает запрос
# \param url			URL-адрес ресурса, пароль от которого необходимо изменить
# \param login			Логин пользователя, используемый для его идентификации на указанном ресурсе
# \param password		Новый пароль от указанного ресурса, на который необходимо заменить существующий
# \returns 				<b>"Authentification error"</b>, если запрос не прошёл аутентификацию
# \returns 				<b>"Your session has already ended"</b>, если сессия пользователя уже была завершена
# \returns				\b 0, если замена пароля произведена успешно
# \returns				<b>Error message</b> – сообщение о непредвиденной ошибке с указаниями возможных действий пользователя по её устранению 
@csrf_exempt		
def change_password(request):
		try:
			if authentificate(request.POST.getlist('auth_seq'), username = request.POST['username']) != 0:
				return HttpResponse("Authentification error!")
			else:
				user_obj = User.objects.get(User_name = request.POST['username'])
				user_obj.Authentication_sequence = None
				user_obj.save()
			user_obj = User.objects.get(User_name = request.POST['username'])
			if(user_obj.Session_started == False):
				return HttpResponse("Your session has already ended")
			url = request.POST['url']
			login = request.POST['login']
			rec = Main_record.objects.get(pair_id = Pair.objects.get(login_id = Login.objects.get(Login = login), resource_id = Resource.objects.get(URL = url)), user_id = User.objects.get(User_name = request.POST['username']))
			rec.Password = request.POST['password']
			rec.Change_date = datetime.datetime.now()
			rec.save()
			return HttpResponse(0)
		except:
			return HttpResponse("POST method is required! Send \'auth_seq\', \'username\', \'url\', \'login\', \'password\'")
			

## Обработчик http-запроса на начало новой сессии работы с программой
#
# Тип запроса: \b POST
#
# Структура запроса: \c URL<b>/startsession/</b>, где \c URL – ip-адрес и порт, на которых развёрнут сервер.
# \param auth_seq 		Список (массив) чисел, представляющий собой байты расшифрованной аутентификационной последовательности, выданной клиентскому приложению
# \param user 			Имя пользователя, от которого поступает запрос
# \param open_key		Открытый ключ пользователя, который должен применяться в начинаемой сессии для аутентификации запросов
# \returns 				<b>"Authentification error"</b>, если запрос не прошёл аутентификацию
# \returns				<b>"Session has already started"</b>, если сессия для этого пользователя уже была начата ранее
# \returns				<b>"Session started"</b>, если сессия начата успешно
# \returns				<b>Error message</b> – сообщение о непредвиденной ошибке с указаниями возможных действий пользователя по её устранению
@csrf_exempt
def start_session(request):
	try:
		if authentificate(request.POST.getlist('auth_seq'), username = request.POST['username']) != 0:
			return HttpResponse("Authentification error!")
		else:
			user_obj = User.objects.get(User_name = request.POST['username'])
			user_obj.Authentication_sequence = None
			user_obj.save()
		username = request.POST['username']
		open_key_array = request.POST.getlist('openkey')
		open_key = b''
		for ch in open_key_array:
			open_key += int(ch).to_bytes(1, byteorder = 'little', signed = False)
		user_obj = User.objects.get(User_name = request.POST['username'])
		if(user_obj.Session_started == True):
			return HttpResponse("Your session has already started")
		user_obj.Open_key = open_key
		user_obj.Session_started = True
		user_obj.save()
		return HttpResponse("Session started")
	except:
		return HttpResponse("POST method is required! Send \'auth_seq\', \'username\', \'openkey\'")
		

## Обработчик http-запроса на завершение текущей сессии работы с программой
#
# Тип запроса: \b POST
#
# Структура запроса: \c URL<b>/startsession/</b>, где \c URL – ip-адрес и порт, на которых развёрнут сервер.
# \param auth_seq 		Список (массив) чисел, представляющий собой байты расшифрованной аутентификационной последовательности, выданной клиентскому приложению
# \param user 			Имя пользователя, от которого поступает запрос
# \returns 				<b>"Authentification error"</b>, если запрос не прошёл аутентификацию
# \returns				<b>"Session has already ended"</b>, если сессия для этого пользователя уже была завершена ранее
# \returns				<b>"Session ended"</b>, если сессия завершена успешно
# \returns				<b>Error message</b> – сообщение о непредвиденной ошибке с указаниями возможных действий пользователя по её устранению		
@csrf_exempt
def end_session(request):
	try:
		if authentificate(request.POST.getlist('auth_seq'), username = request.POST['username']) != 0:
			return HttpResponse("Authentification error!")
		else:
			user_obj = User.objects.get(User_name = request.POST['username'])
			user_obj.Authentication_sequence = None
			user_obj.save()
		username = request.POST['username']
		user_obj = User.objects.get(User_name = request.POST['username'])
		if(user_obj.Session_started == False):
			return HttpResponse("Your session has already ended")
		user_obj.Session_started = False
		user_obj.save()
		return HttpResponse("Session ended")
	except:
		return HttpResponse("POST method is required! Send \'auth_seq\', \'username\'")
		

