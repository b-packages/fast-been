from fast_been.api.models import Base
from fast_been.conf.database import Model

from sqlalchemy import (
    Column,
    String,
)


class Owner(Base, Model):
    __tablename__ = 'owner'

    name = Column(
        String(127),
    )
    server_ip = Column(
        String(31),
    )
