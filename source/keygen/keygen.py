import rsa
from base64 import b64encode

def generate(unique, pubkey, privkey, secret="changeme"):
    if None in [pubkey, privkey]:
        pubkey, privkey = rsa.newkeys(4096)

    data = str([unique, secret])
    sig = rsa.sign(data.encode(), privkey, 'SHA-1')
    license = b64encode(sig).decode('ascii').upper()[:32]

    return license

from functools import partial
gen_license = partial(generate, pubkey=your_pub_key, privkey=your_priv_key, secret="your_secret")
