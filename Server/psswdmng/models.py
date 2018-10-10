from django.db import models

# Create your models here.

class Resource(models.Model):
	resource_id = models.AutoField(primary_key = True, unique = True, null = False)
	URL = models.CharField(max_length = 150, unique = True, null = False)
		
	def __str__(self):
		return self.URL

class Login(models.Model):
	login_id = models.AutoField(primary_key = True, unique = True, null = False)
	Login = models.CharField(max_length = 30, unique = True, null = False)
		
	def __str__(self):
		return self.Login
		
class Pair(models.Model):
	pair_id = models.AutoField(primary_key = True, unique = True, null = False)
	login_id = models.ForeignKey('Login', on_delete = models.CASCADE)
	resource_id = models.ForeignKey('Resource', on_delete = models.CASCADE)
	
	def __str__(self):
		return self.pair_id
		
class Main_record(models.Model):
	pair_id = models.ForeignKey('Pair', on_delete = models.CASCADE, primary_key = True)
	Password = models.CharField(max_length = 50, null = False)
	Change_date = models.DateTimeField(auto_now = True, null = False)
	user_id = models.ForeignKey('User', on_delete = models.CASCADE)
	
	def __str__(self):
		return self.pair_id
	
class User(models.Model):
	user_id = models.AutoField(primary_key = True, unique = True, null = False)
	User_name = models.CharField(max_length = 30, unique = True, null = False)
	Master_password_hash = models.BigIntegerField(null = False)
	