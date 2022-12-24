from beensi_framework.conf.base_settings import BASE_SETTINGS

from .__base import __Base


class Lister(__Base):
    filter_set: list = list()
    order_set: list = list()

    @property
    def pagination(self):
        return BASE_SETTINGS.PAGINATION.IS_ACTIVE

    def page(self, value: int = 1) -> int | None:
        if self.pagination:
            return value
        return None

    def page_size(self, value: int = BASE_SETTINGS.PAGINATION.PAGE_SIZE):
        if self.pagination:
            return value
        return None

    def filters(self, value: dict) -> dict:
        rst = dict()
        for k, v in value.items():
            if k in self.filter_set:
                rst[k] = v
        return rst

    def ordering(self, value: list) -> list:
        rst = list()
        for i in value:
            if i in self.order_set:
                rst.append(i)
        return rst

    def run(self, page: int = None, page_size: int = None, filters: dict = None, ordering: list = None):
        tmp = self.__get(page=page, page_size=page_size, filters=filters, ordering=ordering)
        if not len(tmp):
            return None
        self.validate_data([i.to_dict() for i in tmp], many=True)
        return self.__paginate(self.output)

    def __get(self, page: int, page_size: int, filters: dict, ordering: list):
        rst = self.queryset

        filters = self.filters(filters)
        if filters:
            rst = rst.filter(**filters).all()

        ordering = self.ordering(ordering)
        if ordering:
            rst = rst.order_by(*ordering).all()
        # todo pagination
        return rst

    def __paginate(self, value):
        if not BASE_SETTINGS.PAGINATION.IS_ACTIVE:
            return value
        # todo refactor ...
        return value
