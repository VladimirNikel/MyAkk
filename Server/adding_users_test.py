from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import requests
import time

users = ['pot', 'nikel', 'roman', 'timofey', 'monah', 'monarh', '228nikita', 'kirill654', 'tot456', 'mina234']

def save_key(pk, filename):
    pem = pk.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open(filename, 'wb') as pem_out:
        pem_out.write(pem)


for user in users:
		
	private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
	
	save_key(private_key, user + '.pem')
	
	open_key = private_key.public_key()
	open_key_bytes = open_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)
	open_key_nums = []
	for i in open_key_bytes:
		open_key_nums.append(i)

	r = requests.post('http://127.0.0.1:8000/psswdmng/adduser/', data = {'username' : user, 'passwordhash' : hash('qwerty123'), 'openkey' : open_key_nums})
	
	print(r.text)
	
