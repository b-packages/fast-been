from beensi_framework.utils.schemas.fields import Fields
from beensi_framework.utils.macros import TYPE, BASE


class __Base:
    def __init__(self, db, model):
        self.__db = db
        self.__model = model

    __db = None

    @property
    def db(self):
        return self.__db

    __model = None

    @property
    def model(self):
        return self.__model

    __queryset = None

    @property
    def queryset(self):
        if self.__queryset is None:
            self.__queryset = self.db.query(self.model).filter(is_active=True).all()
        return self.__queryset

    field_control_options: dict = None

    def validate_data(self, **input_data):
        data = {}
        for k, v in input_data:
            data[k] = self.__field_class(k, v)
        return data

    def __field_class(self, k, v):
        field = Fields[BASE]
        base_value_input = {
            'name': k,
            'value': v,
            'queryset': self.queryset,
        }
        if not self.field_control_options:
            return field(**base_value_input)
        if not self.field_control_options[k]:
            return field(**base_value_input)
        if not self.field_control_options[k][TYPE]:
            base_value_input.update(self.field_control_options[k])
            return field(**base_value_input)
        try:
            field = Fields[self.field_control_options[k][TYPE]]
            base_value_input.update(self.field_control_options[k])
            return field(**base_value_input)
        except:
            field = Fields[BASE]
            base_value_input.update(self.field_control_options[k])
            return field(**base_value_input)
