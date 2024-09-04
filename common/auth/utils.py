from django.conf import settings

from common.models import User

import hashlib
import os


def generate_pin(length=6):
    hash_algorithm = "sha512"
    key = getattr(hashlib, hash_algorithm)()
    key.update(getattr(settings, "SECRET_KEY", None).encode("utf-8"))
    key.update(os.urandom(16))
    pin = str(int(key.hexdigest(), 16))[-length:]
    return pin


def sign_uid(uid):
    return User.signer.sign(uid)


def decode_uid_signature(signature, max_age=120):
    return User.signer.unsign(signature, max_age=max_age)
