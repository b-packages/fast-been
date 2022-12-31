from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base as d_base
from sqlalchemy.orm import sessionmaker
from fast_been.conf.base_settings import BASE_SETTINGS

engine = create_engine(
    BASE_SETTINGS.SQLALCHEMY_DATABASE_URL,
    connect_args={
        'check_same_thread': False,
    },
)

session_local = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Model = d_base()


# Dependency
def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


def create_db(base_model, engin):
    base_model.metadata.create_all(bind=engin)
