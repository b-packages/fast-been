from abc import ABC, abstractmethod
from typing import Union
from sqlalchemy.orm import Session

from fast_been.utils.exceptions.http import (
    RequiredInputValueHTTPException,
    AllowNullInputValueHTTPException,
    AllowBlankInputValueHTTPException,
    UniqueInputValueHTTPException,
    RegexValidatorInputValueHTTPException,
    TypeInputValueHTTPException,
    MaximumValueInputValueHTTPException,
    MinimumValueInputValueHTTPException,
    MaximumLengthInputValueHTTPException,
    MinimumLengthInputValueHTTPException,
)
from fast_been.utils.macros import ALL


class Base(ABC):
    model = None
    db: Session = None
    lookup_field_name: str = 'pid'
    field_control_options: Union[dict, None] = None
    input_fields: Union[list, str, None] = None
    output_fields: Union[list, str, None] = None

    @abstractmethod
    def run(self, *args, **kwargs):
        pass

    __queryset_ = None

    @property
    def __queryset(self):
        if self.__queryset_ is None:
            self.__queryset_ = self.db.query(self.model).filter(self.model.is_active == True)
        return self.__queryset_

    def input_data(self, **kwargs):
        if type(self.input_fields) == list:
            return self.__input_for_input_fields(**kwargs)
        if self.input_fields == ALL:
            return self.__input_for_all_fields(**kwargs)
        return {}

    def __input_for_input_fields(self, **kwargs):
        rslt = {}
        for key, value in kwargs.items():
            if key in self.input_fields:
                if key in self.field_control_options:
                    for i in self.field_control_options[key]:
                        if i == 'converter':
                            continue
                        value = self.__field_control_options_mapper_input(controller_name=i, key=key, value=value)
                    if 'converter' in self.field_control_options[key]:
                        value = self.__field_control_options_mapper_input(controller_name='converter', key=key,
                                                                          value=value)
                if value:
                    rslt[key] = value
        return rslt

    def __input_for_all_fields(self, **kwargs):
        rslt = {}
        for key, value in kwargs.items():
            if key in self.field_control_options:
                for i in self.field_control_options[key]:
                    if i == 'converter':
                        continue
                    value = self.__field_control_options_mapper_input(controller_name=i, key=key, value=value)
                if 'converter' in self.field_control_options[key]:
                    value = self.__field_control_options_mapper_input(controller_name='converter', key=key, value=value)
            if value:
                rslt[key] = value
        return rslt

    def output_data(self, **kwargs):
        if type(self.output_fields) == list:
            return self.__output_for_output_fields(**kwargs)
        if self.output_fields == ALL:
            return self.__output_for_all_fields(**kwargs)
        return {}

    def __output_for_output_fields(self, **kwargs):
        rslt = {}
        for key, value in kwargs.items():
            if key in self.output_fields:
                if key in self.field_control_options:
                    for i in self.field_control_options[key]:
                        value = self.__field_control_options_mapper_output(controller_name=i, key=key, value=value)
                if value:
                    rslt[key] = value
        return rslt

    def __output_for_all_fields(self, **kwargs):
        rslt = {}
        for key, value in kwargs.items():
            if key in self.field_control_options:
                for i in self.field_control_options[key]:
                    value = self.__field_control_options_mapper_output(controller_name=i, key=key, value=value)
            if value:
                rslt[key] = value
        return rslt

    def __default(self, key, value):
        if not value:
            return self.field_control_options[key]['default']
        return value

    def __required(self, key, value):
        if self.field_control_options[key]['required'] and value is None:
            raise RequiredInputValueHTTPException(key)
        return value

    def __allow_null(self, key, value):
        if not self.field_control_options[key]['allow_null'] and value is None:
            raise AllowNullInputValueHTTPException(key)
        return value

    def __allow_blank(self, key, value):
        if not self.field_control_options[key]['allow_blank'] and self.__is_blank(value):
            raise AllowBlankInputValueHTTPException(key)
        return value

    def __read_only(self, key, value):
        if self.field_control_options[key]['read_only']:
            return None
        return value

    def __write_only(self, key, value):
        if self.field_control_options[key]['write_only']:
            return None
        return value

    def __unique(self, key, value):
        if self.field_control_options[key]['unique'] and self.retrieve_data(**{key: value}):
            raise UniqueInputValueHTTPException(key)
        return value

    def __regex_validator(self, key, value):
        regex_validator = self.field_control_options[key]['regex_validator']
        if not regex_validator.validate(value):
            raise RegexValidatorInputValueHTTPException(key, regex_validator.info)
        return value

    def __type(self, key, value):
        type_input_value = self.field_control_options[key]['type']
        if not self.__types__controller[type_input_value](value):
            raise TypeInputValueHTTPException(key, type_input_value)
        return value

    def __maximum_value(self, key, value):
        maximum_value = self.field_control_options[key]['maximum_value']
        if not (type(value) in [int, float] and value <= maximum_value):
            raise MaximumValueInputValueHTTPException(key, maximum_value)
        return value

    def __minimum_value(self, key, value):
        minimum_value = self.field_control_options[key]['minimum_value']
        if not (type(value) in [int, float] and minimum_value <= value):
            raise MinimumValueInputValueHTTPException(key, minimum_value)
        return value

    def __maximum_length(self, key, value):
        maximum_length = self.field_control_options[key]['maximum_length']
        if not (type(value) in [str, list, dict, tuple, set] and len(value) <= maximum_length):
            raise MaximumLengthInputValueHTTPException(key, maximum_length)
        return value

    def __minimum_length(self, key, value):
        minimum_length = self.field_control_options[key]['minimum_length']
        if not (type(value) in [str, list, dict, tuple, set] and minimum_length <= len(value)):
            raise MinimumLengthInputValueHTTPException(key, minimum_length)
        return value

    def __converter(self, key, value):
        converter = self.field_control_options[key]['converter']
        return converter(value)

    @staticmethod
    def __is_blank(value):
        if value is None:
            return True
        try:
            return not bool(len(value))
        except:
            return False

    __types__controller_ = None

    @property
    def __types__controller(self):
        if self.__types__controller_:
            return self.__types__controller_
        self.__types__controller_ = {
            'numeric': self.__is_numeric,
            'integer': self.__is_integer,
            'positive_integer': self.__is_positive_integer,
            'negative_integer': self.__is_negative_integer,
            'float': self.__is_float,
            'positive_float': self.__is_positive_float,
            'negative_float': self.__is_negative_float,
            'string': self.__is_string,
            'list': self.__is_list,
            'dictionary': self.__is_dictionary,
            'tuple': self.__is_tuple,
            'set': self.__is_set,
            'boolean': self.__is_boolean,
        }
        return self.__types__controller_

    @staticmethod
    def __is_numeric(value):
        return type(value) in (int, float, complex)

    @staticmethod
    def __is_integer(value):
        return type(value) is int

    @staticmethod
    def __is_positive_integer(value):
        return type(value) is int and 0 <= value

    @staticmethod
    def __is_negative_integer(value):
        return type(value) is int and value <= 0

    @staticmethod
    def __is_float(value):
        return type(value) is float

    @staticmethod
    def __is_positive_float(value):
        return type(value) is float and 0 <= value

    @staticmethod
    def __is_negative_float(value):
        return type(value) is float and value <= 0

    @staticmethod
    def __is_string(value):
        return type(value) is str

    @staticmethod
    def __is_list(value):
        return type(value) is list

    @staticmethod
    def __is_dictionary(value):
        return type(value) is dict

    @staticmethod
    def __is_tuple(value):
        return type(value) is tuple

    @staticmethod
    def __is_set(value):
        return type(value) is set

    @staticmethod
    def __is_boolean(value):
        return type(value) is bool

    __controllers_ = None

    @property
    def __controllers(self):
        if self.__controllers_:
            return self.__controllers_
        self.__controllers_ = {
            'default': self.__default,
            'required': self.__required,
            'allow_null': self.__allow_null,
            'allow_blank': self.__allow_blank,
            'read_only': self.__read_only,
            'write_only': self.__write_only,
            'unique': self.__unique,
            'regex_validator': self.__regex_validator,
            'type': self.__type,
            'maximum_value': self.__maximum_value,
            'minimum_value': self.__minimum_value,
            'maximum_length': self.__maximum_length,
            'minimum_length': self.__minimum_length,
            'converter': self.__converter,
        }
        return self.__controllers_

    def __field_control_options_mapper_input(self, controller_name, key, value):
        if controller_name in ['write_only', ]:
            return value
        return self.__field_control_options_mapper(
            controller_name=controller_name, key=key, value=value)

    def __field_control_options_mapper_output(self, controller_name, key, value):
        if controller_name in ['write_only', ]:
            return self.__field_control_options_mapper(
                controller_name=controller_name, key=key, value=value)
        return value

    def __field_control_options_mapper(self, controller_name, key, value):
        if controller_name in self.__controllers:
            return self.__controllers[controller_name](key=key, value=value)
        return value

    def create_data(self, **kwargs):
        inst = self.model(**kwargs)
        inst.__set_pid(kwargs['pid'] if 'pid' in kwargs else None)
        inst.__set_create_datetime()
        inst.__set_is_active()
        inst.__set_hashed()
        self.db.add(inst)
        self.db.commit()
        self.db.refresh(inst)
        return inst

    def retrieve_data(self, **kwargs):
        return self.__queryset.filter_by(**kwargs).first()

    def destroy_data(self, **kwargs):
        inst = self.retrieve_data(**kwargs)
        if not inst:
            return False
        inst.is_active = False
        self.db.add(inst)
        self.db.commit()
        self.db.refresh(inst)
        return True

    def list_data(self, **kwargs):
        rslt = self.__queryset
        if 'filters' in kwargs:
            rslt = rslt.filter_by(**kwargs['filters']).all()
        if 'ordering' in kwargs:
            rslt = rslt.order_by(*kwargs['ordering']).all()
        return rslt
