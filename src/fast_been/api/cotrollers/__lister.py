import math

from fast_been.conf.base_settings import BASE_SETTINGS

from .__base import __Base


class Lister(__Base):

    def run(self, page: int = None, page_size: int = None, filters: dict = None, ordering: list = None):
        return self.list(page=page, page_size=page_size, filters=filters, ordering=ordering)

    def list(self, page: int = None, page_size: int = None, filters: dict = None, ordering: list = None):
        instances_ = self.__list(
            filters=self.__filters(filters),
            ordering=self.__ordering(ordering)
        )
        if self.__pagination:
            return self.__list_pagination_true(
                instances=instances_,
                page=self.__page(page),
                page_size=self.__page_size(page_size)
            )
        return self.__list_pagination_false(instances=instances_)

    filter_set = []
    order_set = []

    @property
    def __pagination(self):
        return BASE_SETTINGS.PAGINATION.IS_ACTIVE

    def __page(self, value=None):
        if value is None:
            value = 1
        if self.__pagination:
            return value
        return None

    def __page_size(self, value=None):
        if value is None:
            value = BASE_SETTINGS.PAGINATION.PAGE_SIZE
        if self.__pagination:
            return value
        return None

    def __filters(self, value: dict) -> dict:
        rst = dict()
        for k, v in value.items():
            if k in self.filter_set:
                rst[k] = v
        return rst

    def __ordering(self, value: list) -> list:
        rst = list()
        for i in value:
            if i in self.order_set:
                rst.append(i)
        return rst

    def __list_pagination_false(self, instances):
        count = instances.count()
        page_number = 1
        page_size = count
        result = [self.__output(**i.to_dict()) for i in instances]
        next_page = None
        previous_page = None
        rslt = {
            'count': count,
            'page_number': page_number,
            'page_size': page_size,
            'result': result,
            'next_page': next_page,
            'previous_page': previous_page
        }
        return rslt

    def __list_pagination_true(self, instances, page, page_size):
        page = page,
        page_size = page_size
        count = instances.count()
        tmp = instances.paginate(page=page, per_page=page_size)
        result = [self.__output(**i.to_dict()) for i in tmp]
        number_of_pages = math.ceil(count / page_size)
        next_page = self.__next_page(number_of_pages=number_of_pages,
                                     page_size=page_size, current_page_number=page)
        previous_page = self.__previous_page(page_size=page_size, current_page_number=page)
        rslt = {
            'count': count,
            'page_number': page,
            'page_size': page_size,
            'number_of_pages': number_of_pages,
            'next_page': next_page,
            'previous_page': previous_page,
            'result': result,
        }
        return rslt

    @staticmethod
    def __next_page(number_of_pages, page_size, current_page_number):
        if current_page_number < number_of_pages:
            return '?page={}&page_size={}'.format(current_page_number + 1, page_size)
        return None

    @staticmethod
    def __previous_page(page_size, current_page_number):
        if 1 < current_page_number:
            return '?page={}&page_size={}'.format(current_page_number - 1, page_size)
        return None
