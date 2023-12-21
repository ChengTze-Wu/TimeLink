from sqlalchemy import create_engine
from flask import current_app
from sqlalchemy.orm import sessionmaker, Session


_engine = None


def get_engine():
    global _engine
    if _engine is None:
        SQLALCHEMY_DATABASE_URL = current_app.config.get('DATABASE', None)
        ECHO_LOG_ENABLED = current_app.config.get('ECHO_LOG_ENABLED', False)
        _engine = create_engine(url=SQLALCHEMY_DATABASE_URL, echo=ECHO_LOG_ENABLED)
    return _engine


def get_session() -> Session:
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()