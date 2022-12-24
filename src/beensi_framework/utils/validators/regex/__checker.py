import re


def regex_checker(regex_pattern, string: str, error_messages: list):
    if not re.match(regex_pattern, string):
        raise Exception(f'{error_messages}')
