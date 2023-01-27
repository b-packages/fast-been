from sqlalchemy import Integer, Column, String, DateTime, ForeignKey, Text

from fast_been.utils.hahsings import hash_row_db
from fast_been.utils.json import JSON


class Base(object):
    id = Column(Integer, primary_key=True, index=True)
    previous_state = Column(Integer, ForeignKey(id), primary_key=True)
    pid = Column(String, index=True, nullable=False)
    created_datetime = Column(DateTime, nullable=False)
    hashed = Column(Text, nullable=True)

    def to_dict(self) -> dict:
        tmp = self.__all_to_dict().copy()
        tmp.pop('id')
        tmp.pop('hashed')
        return tmp

    def to_json(self) -> str:
        tmp = self.to_dict()
        tmp = JSON.dumps(tmp)
        return tmp

    def hash(self) -> str:
        tmp = self.to_json()
        tmp = hash_row_db(tmp)
        return tmp

    def __all_to_dict(self):
        tmp = dict()
        for column in self.__table__.columns:
            tmp[column.name] = getattr(self, column.name)
        return tmp
