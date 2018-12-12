from django.db import models

# Create your models here.

class Resource(models.Model):
	#resource_id = models.AutoField(primary_key = True, unique = True, null = False)
	resource_id = models.AutoField(primary_key = True)
	URL = models.CharField(max_length = 150, unique = True, null = False)
		
	def __str__(self):
		return self.URL

class Login(models.Model):
	#login_id = models.AutoField(primary_key = True, unique = True, null = False)
	login_id = models.AutoField(primary_key = True)
	Login = models.CharField(max_length = 30, unique = True, null = False)
		
	def __str__(self):
		return self.Login
		
class Pair(models.Model):
	#pair_id = models.AutoField(primary_key = True, unique = True, null = False)
	pair_id = models.AutoField(primary_key = True)
	login_id = models.ForeignKey('Login', on_delete = models.CASCADE)
	resource_id = models.ForeignKey('Resource', on_delete = models.CASCADE)
	
	def __str__(self):
		return self.pair_id
		
class Main_record(models.Model):
	#pair_id = models.ForeignKey('Pair', on_delete = models.CASCADE, primary_key = True)
	pair_id = models.OneToOneField('Pair', on_delete = models.CASCADE, primary_key = True) #fix some shit, servak rugalsya. 
	Password = models.CharField(max_length = 50, null = False)
	Change_date = models.DateTimeField(auto_now = True, null = False)
	user_id = models.ForeignKey('User', on_delete = models.CASCADE)
	
	def __str__(self):
		return self.pair_id
	
class User(models.Model):
	#user_id = models.AutoField(primary_key = True, unique = True, null = False)
        user_id = models.AutoField(primary_key = True)  #esli primary_key -> unique=true i null=false po default
        User_name = models.CharField(max_length = 30, unique = True, null = False)
        Master_password_hash = models.BigIntegerField(null = False)
        Authentication_sequence = models.BinaryField(null = True)
        Open_key = models.BinaryField(null = True)
        Session_started = models.BooleanField(null = False)
	
