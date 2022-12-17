import json

from sqlalchemy import Integer, Boolean, Column, String, DateTime, TEXT

from beensi_framework.utils.generators.db.id import unique_id
from beensi_framework.utils.hahsings import hash_row_db
from beensi_framework.utils.date_time import now


class Base(object):
    id = Column(Integer, primary_key=True, index=True)
    pid = Column(String(255), index=True)
    create_datetime = Column(DateTime())
    hashed = Column(TEXT())
    is_active = Column(Boolean())

    def __set_pid(self):
        self.pid = unique_id()

    def __set_create_datetime(self):
        self.create_datetime = now()

    def __set_hashed(self):
        self.hashed = self.hash()

    def __set_is_active(self):
        self.is_active = True

    def _to_dict(self):
        tmp = dict()
        for column in self.__table__.columns:
            if column.name == 'hashed':
                continue
            tmp[column.name] = str(getattr(self, column.name))
        return tmp

    def to_dict(self):
        tmp = self._to_dict().copy()
        tmp.pop('id')
        tmp.pop('create_datetime')
        tmp.pop('is_active')
        return tmp

    def to_json(self):
        tmp = self.to_dict()
        tmp = json.dumps(tmp)
        return tmp

    def hash(self):
        tmp = self._to_dict()
        tmp = json.dumps(tmp)
        tmp = hash_row_db(tmp)
        return tmp
