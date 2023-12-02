from sqlalchemy import create_engine
from flask import current_app
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = current_app.config.get('DATABASE', None)
ECHO_LOG_ENABLED = current_app.config.get('ECHO_LOG_ENABLED', False)

engine = create_engine(url=SQLALCHEMY_DATABASE_URL, echo=ECHO_LOG_ENABLED)

Session = sessionmaker(bind=engine)
