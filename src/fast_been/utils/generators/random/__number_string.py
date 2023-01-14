from random import randint


def number_string(length: int = 1) -> str:
    tmp = ''
    for i in range(length):
        tmp += str(randint(0, 9))
    return tmp
