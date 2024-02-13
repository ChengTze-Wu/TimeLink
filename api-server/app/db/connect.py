import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE")

if SQLALCHEMY_DATABASE_URL is None:
    raise ValueError("DATABASE Environment Variable is not set")

_engine = None


def get_engine():
    global _engine
    if _engine is None:
        _engine = create_engine(url=SQLALCHEMY_DATABASE_URL, echo=False)
    return _engine


def get_session() -> Session:
    engine = get_engine()
    session = sessionmaker(bind=engine)
    return session()
