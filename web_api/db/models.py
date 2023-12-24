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
import enum

class DayOfWeek(enum.Enum):
    Monday = 1
    Tuesday = 2
    Wednesday = 3
    Thursday = 4
    Friday = 5
    Saturday = 6
    Sunday = 7


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
    description: Mapped[Optional[str]] = mapped_column(Text)

    working_hours: Mapped[List["WorkingHours"]] = relationship(
        "WorkingHours", back_populates="service"
    )

    unavailable_periods: Mapped[List["UnavailablePeriods"]] = relationship(
        "UnavailablePeriods", back_populates="service"
    )

    users: Mapped[List["User"]] = relationship(
        secondary=service_user, back_populates="services"
    )

    groups: Mapped[List["Group"]] = relationship(
        secondary=group_service, back_populates="services"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "image": self.image,
            "description": self.description,
            "working_hours": [working_hour.to_dict() for working_hour in self.working_hours],
            "unavailable_periods": [unavailable_period.to_dict() for unavailable_period in self.unavailable_periods],
            "is_active": self.is_active,
            "is_deleted": self.is_deleted,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class WorkingHours(BaseModel):
    __tablename__ = "working_hours"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    service_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('service.id'))
    day_of_week: Mapped[DayOfWeek] = mapped_column(Integer)
    start_time: Mapped[datetime.time] = mapped_column(DateTime)
    end_time: Mapped[datetime.time] = mapped_column(DateTime)

    service: Mapped["Service"] = relationship("Service", back_populates="working_hours")

    def to_dict(self):
        return {
            "id": self.id,
            "day_of_week": self.day_of_week,
            "start_time": self.start_time,
            "end_time": self.end_time,
        }


class UnavailablePeriods(BaseModel):
    __tablename__ = "unavailable_periods"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    service_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('service.id'))
    start_datetime: Mapped[datetime.datetime]
    end_datetime: Mapped[datetime.datetime]

    service: Mapped["Service"] = relationship("Service", back_populates="unavailable_periods")

    def to_dict(self):
        return {
            "id": self.id,
            "start_datetime": self.start_datetime,
            "end_datetime": self.end_datetime,
        }


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

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "line_group_id": self.line_group_id,
            "is_active": self.is_active,
            "is_deleted": self.is_deleted,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }