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

from .__macro import *


class Base(ABC):
    model = None
    db: Session = None
    lookup_field_name: str = PID
    input_fields: list = list()
    field_control_options: dict = dict()
    output_fields: list = list()

    @abstractmethod
    def controller_type(self):
        pass

    @abstractmethod
    def run(self, *args, **kwargs):
        pass

    @staticmethod
    def __field_control_options_sort_key_func(item):
        return FIELD_CONTROL_OPTIONS_METER[item[0]]

    __get_field_control_options: Union[dict, None] = None

    @property
    def get_field_control_options(self):
        if self.__get_field_control_options:
            return self.__get_field_control_options
        tmp = {}
        for k, v in self.field_control_options.items():
            tmp[k] = dict(sorted(v.items(), key=self.__field_control_options_sort_key_func))
        self.__get_field_control_options = tmp
        return self.__get_field_control_options

    __queryset_ = None

    @property
    def __queryset(self):
        if self.__queryset_ is None:
            self.__queryset_ = self.db.query(self.model).filter(self.model.is_active == True)
        return self.__queryset_

    def input_data(self, **kwargs):
        rslt = {}
        for key, value in kwargs.items():
            if key in self.input_fields:
                if key in self.get_field_control_options:
                    for i in self.get_field_control_options[key]:
                        value = self.__field_control_options_mapper(controller_name=i, key=key, value=value)
                if value:
                    rslt[key] = value
        return rslt

    def output_data(self, **kwargs):
        rslt = {}
        for key, value in kwargs.items():
            if key in self.output_fields and value:
                rslt[key] = value
        return rslt

    def __default(self, key, value):
        if not value:
            return self.get_field_control_options[key][DEFAULT]
        return value

    def __required(self, key, value):
        if self.get_field_control_options[key][REQUIRED] and value is None:
            raise RequiredInputValueHTTPException(key)
        return value

    def __allow_null(self, key, value):
        if not self.get_field_control_options[key][ALLOW_NULL] and value is None:
            raise AllowNullInputValueHTTPException(key)
        return value

    def __allow_blank(self, key, value):
        if not self.get_field_control_options[key][ALLOW_BLANK] and self.__is_blank(value):
            raise AllowBlankInputValueHTTPException(key)
        return value

    def __unique(self, key, value):
        if self.get_field_control_options[key][UNIQUE] and self.retrieve_data(**{key: value}):
            raise UniqueInputValueHTTPException(key)
        return value

    def __regex_validator(self, key, value):
        regex_validator = self.get_field_control_options[key][REGEX_VALIDATOR]
        if not regex_validator.validate(value):
            raise RegexValidatorInputValueHTTPException(key, regex_validator.info)
        return value

    def __type(self, key, value):
        type_input_value = self.get_field_control_options[key][TYPE]
        if type(type_input_value) == str:
            if not self.__types__controller[type_input_value](value):
                raise TypeInputValueHTTPException(key, type_input_value)
            return value
        if type(type_input_value) in [tuple, list]:
            for t in type_input_value:
                if self.__types__controller[t](value):
                    return value
        raise TypeInputValueHTTPException(key, str(type_input_value))

    def __maximum_value(self, key, value):
        maximum_value = self.get_field_control_options[key][MAXIMUM_VALUE]
        if not (type(value) in [int, float] and value <= maximum_value):
            raise MaximumValueInputValueHTTPException(key, maximum_value)
        return value

    def __minimum_value(self, key, value):
        minimum_value = self.get_field_control_options[key][MINIMUM_VALUE]
        if not (type(value) in [int, float] and minimum_value <= value):
            raise MinimumValueInputValueHTTPException(key, minimum_value)
        return value

    def __maximum_length(self, key, value):
        maximum_length = self.get_field_control_options[key][MAXIMUM_LENGTH]
        if not (type(value) in [str, list, dict, tuple, set] and len(value) <= maximum_length):
            raise MaximumLengthInputValueHTTPException(key, maximum_length)
        return value

    def __minimum_length(self, key, value):
        minimum_length = self.get_field_control_options[key][MINIMUM_LENGTH]
        if not (type(value) in [str, list, dict, tuple, set] and minimum_length <= len(value)):
            raise MinimumLengthInputValueHTTPException(key, minimum_length)
        return value

    def __converter(self, key, value):
        converter = self.get_field_control_options[key][CONVERTER]
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
            NUMERIC: self.__is_numeric,
            INTEGER: self.__is_integer,
            POSITIVE_INTEGER: self.__is_positive_integer,
            NEGATIVE_INTEGER: self.__is_negative_integer,
            FLOAT: self.__is_float,
            POSITIVE_FLOAT: self.__is_positive_float,
            NEGATIVE_FLOAT: self.__is_negative_float,
            STRING: self.__is_string,
            LIST: self.__is_list,
            DICTIONARY: self.__is_dictionary,
            TUPLE: self.__is_tuple,
            SET: self.__is_set,
            BOOLEAN: self.__is_boolean,
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
            DEFAULT: self.__default,
            REQUIRED: self.__required,
            ALLOW_NULL: self.__allow_null,
            ALLOW_BLANK: self.__allow_blank,
            TYPE: self.__type,
            UNIQUE: self.__unique,
            MAXIMUM_VALUE: self.__maximum_value,
            MINIMUM_VALUE: self.__minimum_value,
            MAXIMUM_LENGTH: self.__maximum_length,
            MINIMUM_LENGTH: self.__minimum_length,
            REGEX_VALIDATOR: self.__regex_validator,
            CONVERTER: self.__converter,
        }
        return self.__controllers_

    def __field_control_options_mapper(self, controller_name, key, value):
        return self.__controllers[controller_name](
            key=key, value=value) if controller_name in self.__controllers else value

    def create_data(self, **kwargs):
        inst = self.model(**kwargs)
        inst.__set_pid(kwargs[PID] if PID in kwargs else None)
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
        if FILTERS in kwargs:
            rslt = rslt.filter_by(**kwargs[FILTERS]).all()
        if ORDERING in kwargs:
            rslt = rslt.order_by(*kwargs[ORDERING]).all()
        return rslt
