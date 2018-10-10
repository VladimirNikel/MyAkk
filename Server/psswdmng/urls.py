from django.urls import path
from . import views

urlpatterns = [path('', views.index, name = 'index'), 
	path('getpassword/<str:url>/<str:login>/', views.get_password, name = 'get_password'),
	path('adduser/', views.add_user, name = 'add_user'),
	path('authenticate/', views.authenticate, name = 'authenticate'), ]