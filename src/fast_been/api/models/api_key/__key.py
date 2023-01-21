from fast_been.api.models import Base
from fast_been.conf.database import Model

from sqlalchemy import (
    Column,
    String,
    ForeignKey,
)


class Key(Base, Model):
    __tablename__ = 'key'

    owner_id = Column(
        String,
        ForeignKey('owner.id'),
    )
    key = Column(
        String(255),
    )
