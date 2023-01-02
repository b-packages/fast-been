import json

from sqlalchemy import Integer, Boolean, Column, String, DateTime, TEXT

from fast_been.utils.generators.db.id import unique_id
from fast_been.utils.hahsings import hash_row_db
from fast_been.utils.date_time import now


class Base(object):
    id = Column(Integer, primary_key=True, index=True)
    pid = Column(String(255), index=True)
    create_datetime = Column(DateTime())
    hashed = Column(TEXT())
    is_active = Column(Boolean())

    def __set_pid(self, value=None):
        if value:
            self.pid = value
        else:
            self.pid = unique_id()

    def __set_create_datetime(self):
        self.create_datetime = now()

    def __set_hashed(self):
        self.hashed = self.hash()

    def __set_is_active(self):
        self.is_active = True

    def __all_to_dict(self):
        tmp = dict()
        for column in self.__table__.columns:
            tmp[column.name] = getattr(self, column.name)
        return tmp

    def to_dict(self) -> dict:
        tmp = self.__all_to_dict().copy()
        tmp.pop('id')
        tmp.pop('create_datetime')
        tmp.pop('is_active')
        tmp.pop('hashed')
        return tmp

    def to_json(self) -> str:
        tmp = self.to_dict()
        tmp = json.dumps(tmp)
        return tmp

    def hash(self) -> str:
        tmp = self.__all_to_dict()
        tmp.pop('id')
        tmp.pop('is_active')
        tmp.pop('hashed')
        tmp = json.dumps(tmp)
        tmp = hash_row_db(tmp)
        return tmp
