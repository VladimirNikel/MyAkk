from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

import requests

import time


start_time = time.time()

with open("private_key.pem", "rb") as key_file:
    private_key = serialization.load_pem_private_key(key_file.read(), password = None, backend = default_backend())

for j in range(100):	
	r1 = requests.get('http://127.0.0.1:8000/psswdmng/getauthseq/', params = {'user' : 'vvovv'})
	#print('ciphertext: ', r1.content)

	decr_nums = []
	decr_seq = private_key.decrypt(r1.content, padding.OAEP(mgf = padding.MGF1(algorithm = hashes.SHA256()), algorithm = hashes.SHA256(), label = None))
	for b in decr_seq:
		decr_nums.append(b)

	r2 = requests.get('http://127.0.0.1:8000/psswdmng/getpassword/', params = {'user' : 'vvovv', 'auth_seq' : decr_nums, 'url' : 'google.com', 'login' : 'vvovv'})
	print(r2.text)
	
print('time: ', time.time() - start_time)