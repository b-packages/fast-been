from pydantic import root_validator
from beensi_framework.utils.macros import FLOAT

from . import NumericField


class FloatField(NumericField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.TYPE = FLOAT

    number_of_decimal_places: int | None = None

    @root_validator
    def rounded(cls, values):
        if values['value']:
            if values['number_of_decimal_places']:
                values['value'] = round(values['value'], values['number_of_decimal_places'])
        return values
