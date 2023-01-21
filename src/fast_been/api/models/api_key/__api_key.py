from fast_been.api.models import Base
from fast_been.conf.database import Model

from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    DateTime,
)


class ApiKey(Base, Model):
    __tablename__ = 'apikey'

    api_id = Column(
        String,
        ForeignKey('api.id'),
        primary_key=True,
    )
    key_id = Column(
        String,
        ForeignKey('key.id'),
        primary_key=True,
    )
    expiry_datetime = Column(
        DateTime(),
    )
