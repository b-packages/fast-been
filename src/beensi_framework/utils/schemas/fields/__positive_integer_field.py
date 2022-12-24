from pydantic import root_validator
from beensi_framework.utils.macros import MIN_VALUE, POSITIVE_INTEGER

from . import IntegerField


class PositiveIntegerField(IntegerField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.min_value = max(0, kwargs[MIN_VALUE] if MIN_VALUE in kwargs else 0)
        self.TYPE = POSITIVE_INTEGER

    @root_validator
    def check_type(cls, values):
        values = super().check_type(values)
        if values['value']:
            if values['value'] < 0:
                raise Exception(f'Type \"{values["name"]}\" should be \"{values["TYPE"]}\".')
        return values
