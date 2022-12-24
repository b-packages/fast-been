from pydantic import BaseModel, root_validator
from typing import Any


class BaseField(BaseModel):
    name: str
    value: Any = None
    queryset: Any
    unique: bool = False

    @root_validator
    def check_unique(cls, values):
        if values['value']:
            if values['unique'] is True:
                if values['queryset'].filter(**{values['name']: values['value']}).first() is None:
                    raise Exception(f'\"{values["name"]}\" is exist.')
        return values
