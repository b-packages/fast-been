from uuid import uuid4


def unique_id():
    return f'{uuid4().hex}{uuid4().hex}'
