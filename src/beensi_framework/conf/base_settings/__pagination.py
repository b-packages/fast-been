from pydantic import BaseModel as BModel


class __Pagination(BModel):
    IS_ACTIVE: bool = False
    PAGE_SIZE: int = 25
