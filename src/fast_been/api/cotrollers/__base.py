from abc import ABC, abstractmethod
from typing import Union, Optional
from sqlalchemy.orm import Session

from fast_been.utils.schemas.controller.list import OutputList as OutputListSchema
from fast_been.utils.generators.db.id import unique_id
from fast_been.conf.base_settings import BASE_SETTINGS
from fast_been.utils.exceptions.http import *
from fast_been.utils.date_time import now

from .__macro import *


class Base(ABC):
    model = None
    db: Session = None
    lookup_field_name: str = PID
    input_fields: list = list()
    field_control_options: dict = dict()
    output_fields: list = list()
    least_one_required: Optional[list] = None
    pagination: bool = False
    filter_set = []
    order_set = []

    @abstractmethod
    def run(self, *args, **kwargs):
        pass

    @abstractmethod
    def controller_type(self):
        pass

    def input_data(self, **kwargs):
        input_data = {}
        for i in self.input_fields:
            input_data[i] = kwargs[i] if i in kwargs else None
        rslt = {}
        for key, value in input_data.items():
            if key in self.__get_field_control_options:
                for i in self.__get_field_control_options[key]:
                    value = self.__field_control_options_mapper(controller_name=i, key=key, value=value)
            if value:
                rslt[key] = value
        rslt = self.__least_one_required(rslt)
        return rslt

    def output_data(self, **kwargs):
        rslt = {}
        for key, value in kwargs.items():
            if key in self.output_fields and value:
                rslt[key] = value
        return rslt

    def retrieve_data(self, **kwargs):
        obj = self.__retrieve_base(**kwargs)
        return obj

    def create_data(self, **kwargs):
        inst = self.__create_base(**kwargs)
        obj = self.__save_base(inst)
        return obj

    def update_data(self, lookup_field, **kwargs):
        obj = self.__retrieve_base(**{self.lookup_field_name: lookup_field})
        if obj is None:
            return None
        if not len(kwargs):
            return obj
        data = obj.to_dict()
        data.update(kwargs)
        inst = self.__create_base(**data)
        inst.previous_state = obj
        obj = self.__save_base(inst)
        return obj

    def destroy_data(self, lookup_field):
        obj = self.__retrieve_base(**{self.lookup_field_name: lookup_field})
        if obj is None:
            return None
        data = obj.to_dict()
        inst = self.__create_base(**data)
        inst.previous_state = obj
        inst.deleted = True
        obj = self.__save_base(inst)
        return obj

    def list_data(self, filters: dict = None, ordering: list = None, **kwargs):
        qryst = self.__queryset
        flts = self.__filters(filters)
        ords = self.__ordering(ordering)
        qryst = qryst.filter_by(**flts) if flts else qryst
        qryst = qryst.filter_by(*ords) if ords else qryst
        return self.__paginate(qryst, **kwargs)

    def __paginate(self, query_set, page=None, page_size=None):
        if not self.__pagination:
            return query_set.all()
        cnt = query_set.count()
        cpg = self.__page(page)
        pgs = self.__page_size(page_size) or cnt
        tmp = query_set.all() if cnt == pgs else query_set.paginate(page=cpg, per_page=pgs).all()
        rslt = [self.output_data(**i.to_dict()) for i in tmp]
        ret = OutputListSchema(
            count=cnt,
            page_number=cpg,
            page_size=pgs,
            result=rslt,
        )
        return ret.dict()

    __field_control_options_: Union[dict, None] = None
    __queryset_ = None
    __types__controller_ = None
    __controllers_ = None
    __pagination_ = None
    __page_ = None
    __page_size_ = None
    __filters_ = None
    __ordering_ = None

    @staticmethod
    def __field_control_options_sort_key_func(item):
        return FIELD_CONTROL_OPTIONS_METER[item[0]]

    @property
    def __get_field_control_options(self):
        if self.__field_control_options_:
            return self.__field_control_options_
        tmp = {}
        for k, v in self.field_control_options.items():
            tmp[k] = dict(sorted(v.items(), key=self.__field_control_options_sort_key_func))
        self.__field_control_options_ = tmp
        return self.__field_control_options_

    @property
    def __queryset(self):
        if self.__queryset_ is None:
            self.__queryset_ = self.db.query(self.model).filter_by(deleted=False, next_state=None)
        return self.__queryset_

    def __default(self, key, value):
        if not value:
            return self.__get_field_control_options[key][DEFAULT]
        return value

    def __required(self, key, value):
        if self.__get_field_control_options[key][REQUIRED] and value is None:
            raise RequiredInputValueHTTPException(key)
        return value

    def __allow_null(self, key, value):
        if not self.__get_field_control_options[key][ALLOW_NULL] and value is None:
            raise AllowNullInputValueHTTPException(key)
        return value

    def __allow_blank(self, key, value):
        if not self.__get_field_control_options[key][ALLOW_BLANK] and self.__is_blank(value):
            raise AllowBlankInputValueHTTPException(key)
        return value

    def __unique(self, key, value):
        if self.__get_field_control_options[key][UNIQUE] and self.retrieve_data(**{key: value}):
            raise UniqueInputValueHTTPException(key)
        return value

    def __regex_validator(self, key, value):
        regex_validator = self.__get_field_control_options[key][REGEX_VALIDATOR]
        if not regex_validator.validate(value):
            raise RegexValidatorInputValueHTTPException(key, regex_validator.info)
        return value

    def __type(self, key, value):
        type_input_value = self.__get_field_control_options[key][TYPE]
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
        maximum_value = self.__get_field_control_options[key][MAXIMUM_VALUE]
        if not (type(value) in [int, float] and value <= maximum_value):
            raise MaximumValueInputValueHTTPException(key, maximum_value)
        return value

    def __minimum_value(self, key, value):
        minimum_value = self.__get_field_control_options[key][MINIMUM_VALUE]
        if not (type(value) in [int, float] and minimum_value <= value):
            raise MinimumValueInputValueHTTPException(key, minimum_value)
        return value

    def __maximum_length(self, key, value):
        maximum_length = self.__get_field_control_options[key][MAXIMUM_LENGTH]
        if not (type(value) in [str, list, dict, tuple, set] and len(value) <= maximum_length):
            raise MaximumLengthInputValueHTTPException(key, maximum_length)
        return value

    def __minimum_length(self, key, value):
        minimum_length = self.__get_field_control_options[key][MINIMUM_LENGTH]
        if not (type(value) in [str, list, dict, tuple, set] and minimum_length <= len(value)):
            raise MinimumLengthInputValueHTTPException(key, minimum_length)
        return value

    def __converter(self, key, value):
        converter = self.__get_field_control_options[key][CONVERTER]
        return converter(value)

    def __least_one_required(self, input_data: dict):
        if self.least_one_required is None:
            return input_data
        for k, v in input_data.items():
            if k in self.least_one_required:
                return input_data
        raise LeastOneRequiredHTTPException(self.least_one_required)

    @staticmethod
    def __is_blank(value):
        if value is None:
            return True
        try:
            return not bool(len(value))
        except:
            return False

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

    @staticmethod
    def __default_controller(value, **kwargs):
        return value

    def __field_control_options_mapper(self, controller_name, key, value):
        controller = self.__default_controller
        if controller_name in self.__controllers:
            controller = self.__controllers[controller_name]
        ret = controller(key=key, value=value)
        return ret

    def __retrieve_base(self, **kwargs):
        obj = self.__queryset.filter_by(**kwargs).order_by(self.model.id.desc()).first()
        return obj

    def __create_base(self, **kwargs):
        inst = self.model(**kwargs)
        inst.pid = kwargs.get(PID) or unique_id()
        inst.created_datetime = now()
        inst.previous_state = None
        inst.deleted = False
        return inst

    def __save_base(self, instance):
        instance.hashed = instance.hash()
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance

    @property
    def __pagination(self) -> bool:
        if self.__pagination_ is not None:
            return self.__pagination_
        self.__pagination_ = self.pagination or BASE_SETTINGS.PAGINATION.IS_ACTIVE
        return self.__pagination_

    def __page(self, value: int = None) -> Optional[int]:
        if self.__page_:
            return self.__page_
        value = value or BASE_SETTINGS.PAGINATION.DEFAULT_START_PAGE_NUMBER
        self.__page_ = value if self.__pagination else 1
        return self.__page_

    def __page_size(self, value: int = None) -> Optional[int]:
        if self.__page_size_:
            return self.__page_size_
        value = value or BASE_SETTINGS.PAGINATION.PAGE_SIZE
        self.__page_size_ = value if self.__pagination else None
        return self.__page_size_

    def __filters(self, value: dict) -> Optional[dict]:
        if self.__filters_:
            return self.__filters_
        if value is None:
            rst = None
        else:
            rst = dict()
            for k, v in value.items():
                if k in self.filter_set:
                    rst[k] = v
        self.__filters_ = rst
        return self.__filters_

    def __ordering(self, value: list) -> Optional[list]:
        if self.__ordering_:
            return self.__ordering_
        if value is None:
            rst = None
        else:
            rst = list()
            for i in value:
                if i in self.order_set:
                    rst.append(i)
        self.__ordering_ = rst
        return self.__ordering_
