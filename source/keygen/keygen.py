from os import urandom
from hashlib import sha256

def generate(unique, secret="changeme"):
    r = urandom(4096)
    data = str([unique, secret]) + str(r)
    shasum = sha256(data.encode())
    license = shasum.hexdigest().upper()[:32]

    return license
