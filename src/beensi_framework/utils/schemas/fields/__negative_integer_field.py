from pydantic import root_validator

from . import IntegerField
from beensi_framework.utils.macros import MAX_VALUE, NEGATIVE_INTEGER


class NegativeIntegerField(IntegerField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.max_value = min(0, kwargs[MAX_VALUE] if MAX_VALUE in kwargs else 0)
        self.TYPE = NEGATIVE_INTEGER

    @root_validator
    def check_type(cls, values):
        values = super().check_type(values)
        if values['value']:
            if 0 < values['value']:
                raise Exception(f'Type \"{values["name"]}\" should be \"{values["TYPE"]}\".')
        return values
