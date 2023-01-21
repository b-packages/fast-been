from fast_been.api.models import Base
from fast_been.conf.database import Model

from sqlalchemy import Column, String


class Api(Base, Model):
    __tablename__ = 'api'

    url_pattern = Column(
        String(255),
    )
