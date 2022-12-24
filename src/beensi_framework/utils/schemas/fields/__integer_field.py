from pydantic import root_validator

from . import NumericField
from beensi_framework.utils.macros import INTEGER


class IntegerField(NumericField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.TYPE = INTEGER

    @root_validator
    def check_type(cls, values):
        if values['value']:
            if type(values['value']) not in [int]:
                raise Exception(f'Type \"{values["name"]}\" should be \"{values["TYPE"]}\".')
        return values
