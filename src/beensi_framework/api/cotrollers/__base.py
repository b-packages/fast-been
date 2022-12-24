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

    __valid_data: list | dict | None = None

    @property
    def valid_data(self):
        return self.__valid_data

    def validate_data(self, data: list | dict, many=False) -> list | dict:
        if not many:
            return self.__validate_data_many_false(data)
        return self.__validate_data_many_true(data)

    def __validate_data_many_false(self, data: dict) -> dict:
        valid_data = dict()
        for k, v in data.items():
            valid_data[k] = self.__field_class(k, v)
        self.__valid_data = valid_data
        return valid_data

    def __validate_data_many_true(self, data: list) -> list:
        valid_data = list()
        for itm in data:
            tmp = dict()
            for k, v in itm.items():
                tmp[k] = self.__field_class(k, v)
            valid_data.append(tmp)
        self.__valid_data = valid_data
        return valid_data

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

    output_field_list: list | None = None

    def output(self, many=False) -> dict | list | None:
        if not self.valid_data:
            return None
        if not many:
            return self.__output_many_false
        return self.__output_many_true

    @property
    def __output_many_false(self) -> dict:
        rst = {}
        for f in self.valid_data:
            if f.name in self.output_field_list:
                if f.write_only is False:
                    rst[f.name] = f.value
        return rst

    @property
    def __output_many_true(self) -> list:
        rst = []
        for itm in self.valid_data:
            tmp = {}
            for f in itm:
                if f.name in self.output_field_list:
                    if f.write_only is False:
                        tmp[f.name] = f.value
            rst.append(tmp)
        return rst

    def input(self, many=False) -> dict | list | None:
        if not self.valid_data:
            return None
        if not many:
            return self.__input_many_false
        return self.__input_many_true

    @property
    def __input_many_false(self):
        rst = {}
        for f in self.valid_data:
            if f.read_only is False:
                rst[f.name] = f.value
        return rst

    @property
    def __input_many_true(self):
        rst = []
        for itm in self.valid_data:
            tmp = {}
            for f in itm:
                if f.read_only is False:
                    tmp[f.name] = f.value
            rst.append(tmp)
        return rst
