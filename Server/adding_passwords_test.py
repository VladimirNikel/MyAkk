from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key
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
		
def load_key(filename):
    with open(filename, 'rb') as pem_in:
        pemlines = pem_in.read()
    private_key = load_pem_private_key(pemlines, None, default_backend())
    return private_key

for user in users:

	print(user)

	private_key = load_key(user + '.pem')
	
	r = requests.get('http://127.0.0.1:8000/psswdmng/getauthseq/', params = {'username' : user})

	seq_bytes = r.content
	
	#print(r.text)

	plain_bytes = private_key.decrypt(seq_bytes, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))

	auth_seq = []

	for b in plain_bytes:
		auth_seq.append(b)

	r = requests.post('http://127.0.0.1:8000/psswdmng/addpassword/', data = {'username' : user, 'password' : '12345', 'url' : 'yandex.ru', 'login' : user, 'auth_seq' : auth_seq})
	
	print(r.text)
