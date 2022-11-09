import re

from fastapi import HTTPException


def regex_checker(regex_pattern, string: str, error_messages: list):
    if not re.match(regex_pattern, string):
        raise HTTPException(
            status_code=400, detail={'messages': error_messages})
