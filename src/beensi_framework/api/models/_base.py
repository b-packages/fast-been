import json

from sqlalchemy import Boolean, Column, String, DateTime, TEXT

from beensi_framework.utils.generators.db.id import unique_id
from beensi_framework.utils.hahsings import hash_row_db
from beensi_framework.utils.date_time import now


class Base(object):
    id = Column(String(255), primary_key=True, index=True)
    create_datetime = Column(DateTime())
    hashed = Column(TEXT())
    is_active = Column(Boolean())

    def __set_id(self):
        self.id = unique_id()

    def __set_create_datetime(self):
        self.create_datetime = now()

    def __set_hashed(self):
        self.hashed = self.hash()

    def __set_is_active(self):
        self.is_active = True

    def to_dict(self):
        tmp = dict()
        for column in self.__table__.columns:
            tmp[column.name] = str(getattr(self, column.name))
        return tmp

    def to_json(self):
        tmp = self.to_dict()
        tmp = json.dumps(tmp)
        return tmp

    def hash(self):
        tmp = self.to_dict()
        tmp.pop('is_active')
        tmp = json.dumps(tmp)
        tmp = hash_row_db(tmp)
        return tmp

    @classmethod
    def create_object(cls, *args, **kwargs):
        obj = cls(*args, **kwargs)
        obj.__set_id()
        obj.__set_create_datetime()
        obj.__set_is_active()
        return obj

    def create(self, db, *args, **kwargs):
        obj = self.create_object(*args, **kwargs)
        self.__set_hashed()
        db.add(obj)
        db.commit()
        db.referesh(obj)
        return obj
