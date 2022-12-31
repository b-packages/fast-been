from hashlib import sha512


def hash_row_db(value: str) -> str:
    return sha512(value.encode('utf-8')).digest().hex()
