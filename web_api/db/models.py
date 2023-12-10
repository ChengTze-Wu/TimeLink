from typing import List, Optional
import datetime, uuid
from sqlalchemy import (
    ForeignKey,
    Text,
    Column,
    Table,
    DateTime,
    Boolean,
    Integer,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


class BaseModel(DeclarativeBase):
    pass

service_user = Table(
    "service_user_account",
    BaseModel.metadata,
    Column("service_id", ForeignKey("service.id"), primary_key=True),
    Column("user_id", ForeignKey("user_account.id"), primary_key=True),
    Column("reserved_at", DateTime, nullable=True),
    Column("quantity", Integer, nullable=True),
    Column("is_canceled", Boolean, default=False),
    Column("created_at", DateTime, default=datetime.datetime.now, nullable=False),
    Column(
        "updated_at",
        DateTime,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now,
        nullable=False,
    ),
)

group_user = Table(
    "line_group_user",
    BaseModel.metadata,
    Column("group_id", ForeignKey("line_group.id"), primary_key=True),
    Column("user_id", ForeignKey("user_account.id"), primary_key=True),
    Column("created_at", DateTime, default=datetime.datetime.now, nullable=False),
    Column(
        "updated_at",
        DateTime,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now,
        nullable=False,
    ),
)

group_service = Table(
    "line_group_service",
    BaseModel.metadata,
    Column("group_id", ForeignKey("line_group.id"), primary_key=True),
    Column("service_id", ForeignKey("service.id"), primary_key=True),
    Column("created_at", DateTime, default=datetime.datetime.now, nullable=False),
    Column(
        "updated_at",
        DateTime,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now,
        nullable=False,
    ),
)


class CommonColumns:
    __abstract__ = True

    is_active: Mapped[bool] = mapped_column(default=True)
    is_deleted: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now)
    updated_at: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now, onupdate=datetime.datetime.now
    )


class Service(BaseModel, CommonColumns):
    __tablename__ = "service"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(Text)
    price: Mapped[Optional[float]]
    image: Mapped[Optional[str]] = mapped_column(Text)
    period_time: Mapped[Optional[int]]
    open_time: Mapped[Optional[datetime.time]]
    close_time: Mapped[Optional[datetime.time]]
    start_date: Mapped[Optional[datetime.date]]
    end_date: Mapped[Optional[datetime.date]]
    unavailable_datetime: Mapped[Optional[datetime.datetime]]

    users: Mapped[List["User"]] = relationship(
        secondary=service_user, back_populates="services"
    )

    groups: Mapped[List["Group"]] = relationship(
        secondary=group_service, back_populates="services"
    )


class User(BaseModel, CommonColumns):
    __tablename__ = "user_account"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(Text, unique=True)
    username: Mapped[str] = mapped_column(Text, unique=True)
    password: Mapped[str] = mapped_column(Text)
    name: Mapped[str] = mapped_column(Text)
    line_user_id: Mapped[Optional[str]] = mapped_column(
        Text, unique=True, comment="User Id For Line"
    )
    phone: Mapped[Optional[str]] = mapped_column(Text)

    services: Mapped[List[Service]] = relationship(
        secondary=service_user, back_populates="users"
    )

    groups: Mapped[List["Group"]] = relationship(
        secondary=group_user, back_populates="users"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "password": self.password,
            "name": self.name,
            "line_user_id": self.line_user_id,
            "phone": self.phone,
            "is_active": self.is_active,
            "is_deleted": self.is_deleted,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class Group(BaseModel, CommonColumns):
    __tablename__ = "line_group"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(Text)
    line_group_id: Mapped[str] = mapped_column(
        Text, unique=True, comment="Group Id For Line"
    )

    users: Mapped[List[User]] = relationship(
        secondary=group_user, back_populates="groups"
    )

    services: Mapped[List[Service]] = relationship(
        secondary=group_service, back_populates="groups"
    )