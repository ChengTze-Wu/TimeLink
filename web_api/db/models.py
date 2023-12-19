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


class UnavailablePeriod(BaseModel, CommonColumns):
    __tablename__ = "unavailable_period"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    service_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('service.id'))
    start_datetime: Mapped[datetime.datetime]  # 不可預約時間段的開始
    end_datetime: Mapped[datetime.datetime]    # 不可預約時間段的結束

    service: Mapped["Service"] = relationship("Service", back_populates="unavailable_periods")


class Service(BaseModel, CommonColumns):
    __tablename__ = "service"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(Text)
    price: Mapped[Optional[float]]
    image: Mapped[Optional[str]] = mapped_column(Text)
    period_time: Mapped[Optional[int]]  # 作業時間(分鐘)
    open_time: Mapped[Optional[datetime.time]]  # 每日開始時間
    close_time: Mapped[Optional[datetime.time]] # 每日結束時間
    start_date: Mapped[Optional[datetime.date]] # 開始日期
    end_date: Mapped[Optional[datetime.date]]   # 結束日期
    
    unavailable_periods: Mapped[List["UnavailablePeriod"]] = relationship(
        "UnavailablePeriod", back_populates="service"
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
            "period_time": self.period_time,
            "open_time": self.open_time,
            "close_time": self.close_time,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "unavailable_datetime": self.unavailable_datetime,
            "is_active": self.is_active,
            "is_deleted": self.is_deleted,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
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