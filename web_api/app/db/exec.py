from .connect import get_engine
from .models import BaseModel

engine = get_engine()


def init_db():
    """Initialize the database by creating all tables."""
    BaseModel.metadata.create_all(engine)


def drop_db():
    """Drop all tables in the database."""
    BaseModel.metadata.drop_all(engine)


def reset_db():
    """Reset the database by dropping all tables and recreating them."""
    BaseModel.metadata.drop_all(engine)
    BaseModel.metadata.create_all(engine)
