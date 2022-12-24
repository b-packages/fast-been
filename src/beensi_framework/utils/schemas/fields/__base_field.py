from pydantic import BaseModel, root_validator
from typing import Any
from beensi_framework.utils.validators.regex import regex_checker
from .__regex_validator import RegExValidator


class BaseField(BaseModel):
    name: str
    value: Any = None
    TYPE: Any = None
    default: Any = None
    required: bool = False
    allow_null: bool = True
    allow_blank: bool = True
    regex_validator: RegExValidator | None = None

    @root_validator
    def set_default(cls, values):
        values['value'] = values['value'] or values['default']
        return values

    @root_validator
    def check_required(cls, values):
        if values['required'] is True:
            if values['value'] is None:
                raise Exception(f'\"{values["name"]}\" is required.')
        return values

    @root_validator
    def check_allow_null(cls, values):
        if values['allow_null'] is False:
            if values['value'] is None:
                raise Exception(f'\"{values["name"]}\" cannot be null.')
        return values

    @root_validator
    def check_allow_blank(cls, values):
        if values['allow_blank'] is False:
            if values['value'] is not None:
                if not len(str(values['value']).strip()):
                    raise Exception(f'\"{values["name"]}\" cannot be blank.')
        return values

    @root_validator
    def check_regex_validator(cls, values):
        if values['regex_validator']:
            regex_checker(
                string=str(values['value']),
                regex_pattern=values['regex_validator'].pattern,
                error_messages=values['regex_validator'].error_messages
            )
        return values
