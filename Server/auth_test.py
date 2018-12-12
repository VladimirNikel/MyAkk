from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

import requests

import time

user = 'Vova'

start_time = time.time()

from cryptography.hazmat.primitives.serialization import load_pem_private_key

def load_key(filename):
    with open(filename, 'rb') as pem_in:
        pemlines = pem_in.read()
    private_key = load_pem_private_key(pemlines, None, default_backend())
    return private_key

private_key = load_key(user + ".pem")

for j in range(1000):	
	r1 = requests.get('http://127.0.0.1:8000/psswdmng/getauthseq/', params = {'username' : user})
	#print(r1.text)

	decr_nums = []
	decr_seq = private_key.decrypt(r1.content, padding.OAEP(mgf = padding.MGF1(algorithm = hashes.SHA256()), algorithm = hashes.SHA256(), label = None))
	for b in decr_seq:
		decr_nums.append(b)

	r2 = requests.get('http://127.0.0.1:8000/psswdmng/getpassword/', params = {'username' : user, 'auth_seq' : decr_nums, 'url' : 'yandex.ru', 'login' : user})
	
	print(r2.text)
	
print('time: ', time.time() - start_time)