from pydantic import root_validator
from beensi_framework.utils.macros import STRING, MIN_LENGTH

from . import BaseField


class StringField(BaseField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = STRING
        self.min_length = max(0, kwargs[MIN_LENGTH] if MIN_LENGTH in kwargs else 0)

    min_length: int = 0
    max_length: int | None = None

    @root_validator
    def check_max_length(cls, values):
        if values['value']:
            if values['max_length']:
                if values['max_length'] < len(values['value']):
                    raise Exception(
                        f"The length of \"{values['name']}\" must be less than "
                        f"or equal to the number of \"{values['max_length']}\"."
                    )
        return values

    @root_validator
    def check_min_length(cls, values):
        if values['value']:
            if len(values['value']) < values['min_length']:
                raise Exception(
                    f"The length of \"{values['name']}\" must be greater than "
                    f"or equal to the number of \"{values['min_length']}\"."
                )
        return values

    @root_validator
    def check_type(cls, values):
        if values['value']:
            if type(values['value']) not in [str]:
                raise Exception(f'Type \"{values["name"]}\" should be \"{values["TYPE"]}\".')
        return values
