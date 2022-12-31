from hashlib import sha512


def hashed_password(password: str) -> str:
    return sha512(password.encode('utf-8')).digest().hex()
