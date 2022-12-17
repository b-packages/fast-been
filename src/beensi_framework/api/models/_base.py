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

    def set_controller_fields(self):
        self.__set_id()
        self.__set_create_datetime()
        self.__set_is_active()
        self.__set_hashed()

    @classmethod
    def create(cls, db, **kwargs):
        obj = cls(**kwargs)
        obj.set_controller_fields()
        db.add(obj)
        db.commit()
        db.referesh(obj)
        return obj
