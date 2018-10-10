from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def index(request):
	return HttpResponse("You're in start page")

def get_password(request, url, login):
	result = Main_record.objects.get(pair_id = Pair.objects.get(login_id = Login.objects.get(Login = login), resource_id = Resource.objects.get(URL = url)))
	return HttpResponse(result.Password)

@csrf_exempt	
def add_user(request):
	username = request.POST['username']
	passwordhash = request.POST['passwordhash']
	User.objects.create(User_name = username, Master_password_hash = passwordhash)
	return HttpResponse(0)
	
def authenticate(request):
	print(request.GET)
	username = request.GET['username']
	passwordhash = request.GET['passwordhash']
	user = User.objects.get(User_name = username)
	if str(user.Master_password_hash) == passwordhash:
		return HttpResponse(1)
	else:
		return HttpResponse(0)
