from django.urls import path
from . import views

urlpatterns = [path('', views.index, name = 'index'), 
	path('addpassword/', views.add_password, name = 'add_password'),
	path('getpassword/', views.get_password, name = 'get_password'),
	path('adduser/', views.add_user, name = 'add_user'),
	path('authenticate/', views.authenticate, name = 'authenticate'),
	path('getauthseq/', views.get_authentication_sequence, name = 'get_authentication_sequence'),
	path('changepassword/', views.change_password, name = 'change_password'),
	path('startsession/', views.start_session, name = 'start_session'),
	path('endsession/', views.end_session, name = 'end_session'),]