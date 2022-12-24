from pydantic import root_validator
from beensi_framework.utils.macros import NUMERIC

from . import BaseField


class NumericField(BaseField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.TYPE = NUMERIC

    max_value: int | None = None
    min_value: int | None = None

    @root_validator
    def check_max_value(cls, values):
        if values['value']:
            if values['max_value']:
                if values['max_value'] < values['value']:
                    raise Exception(
                        f"The value of \"{values['name']}\" must be"
                        f" less than or equal to the value of \"{values['max_value']}\"."
                    )
        return values

    @root_validator
    def check_min_value(cls, values):
        if values['value']:
            if values['min_value']:
                if values['value'] < values['min_value']:
                    raise Exception(
                        f"The value of \"{values['name']}\" must be"
                        f" greater than or equal to the value of \"{values['min_value']}\"."
                    )
        return values

    @root_validator
    def check_type(cls, values):
        if values['value']:
            if type(values['value']) not in [int, float]:
                raise Exception(f'Type \"{values["name"]}\" should be \"{values["TYPE"]}\".')
        return values
