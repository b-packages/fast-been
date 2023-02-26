from pydantic import BaseModel as BModel


class __Pagination(BModel):
    IS_ACTIVE: bool = False
    PAGE_SIZE: int = 25
    DEFAULT_START_PAGE_NUMBER: int = 1
    ORDERING: list = []
