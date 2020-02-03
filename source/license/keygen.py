from os import urandom
from hashlib import sha256
from django.conf import settings

def generate(unique, secret=settings.LICENSE_SECRET):
    r = urandom(4096)
    data = str([unique, secret]) + str(r)
    shasum = sha256(data.encode())
    license = shasum.hexdigest().upper()[:32]

    return license

def gen_many(l):
    # l is an iterator of size n of which a list of n keys will be returned
    # using the iterator values as unique. an easy way to use it is to just call
    # gen_many(range(n)) where n is how many keys you want to generate, but you
    # should probably supply something *actually* unique and not just ints
    # alternatively, just call generate() directly, it's quite fast anyways

    return list(map(generate, l))
