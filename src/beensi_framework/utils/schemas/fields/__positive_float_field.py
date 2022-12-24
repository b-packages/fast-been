from pydantic import root_validator
from beensi_framework.utils.macros import POSITIVE_FLOAT, MIN_VALUE

from . import FloatField


class PositiveFloatField(FloatField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.min_value = max(0, kwargs[MIN_VALUE] if MIN_VALUE in kwargs else 0)
        self.TYPE = POSITIVE_FLOAT

    @root_validator
    def check_type(cls, values):
        values = super().check_type(values)
        if values['value']:
            if values['value'] < 0:
                raise Exception(f'Type \"{values["name"]}\" should be \"{values["TYPE"]}\".')
        return values
