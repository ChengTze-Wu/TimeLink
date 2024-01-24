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
    Time,
    Enum as SQLAlchemyEnum,
    UUID,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)
import enum


class DayOfWeek(enum.Enum):
    Monday = "Monday"
    Tuesday = "Tuesday"
    Wednesday = "Wednesday"
    Thursday = "Thursday"
    Friday = "Friday"
    Saturday = "Saturday"
    Sunday = "Sunday"


class RoleName(enum.Enum):
    ADMIN = "admin"
    GROUP_OWNER = "group_owner"
    GROUP_MEMBER = "group_member"


class BaseModel(DeclarativeBase):
    pass


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
    working_period: Mapped[Optional[int]] = mapped_column(Integer)

    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user_account.id"))

    working_hours: Mapped[List["WorkingHour"]] = relationship(
        "WorkingHour", back_populates="service"
    )

    unavailable_periods: Mapped[List["UnavailablePeriod"]] = relationship(
        "UnavailablePeriod", back_populates="service"
    )

    appointments: Mapped[List["Appointment"]] = relationship(
        "Appointment", back_populates="service"
    )

    groups: Mapped[List["Group"]] = relationship(
        secondary=group_service, back_populates="services"
    )

    owner: Mapped["User"] = relationship("User", back_populates="own_services")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "image": self.image,
            "description": self.description,
            "working_period": self.working_period,
            "owner": self.owner.to_self_dict() if self.owner else None,
            "working_hours": [working_hour.to_dict() for working_hour in self.working_hours],
            "unavailable_periods": [unavailable_period.to_dict() for unavailable_period in self.unavailable_periods],
            "is_active": self.is_active,
            "is_deleted": self.is_deleted,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "groups" : [group.to_self_dict() for group in self.groups],
        }
    
    def to_self_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "image": self.image,
            "description": self.description,
            "working_period": self.working_period,
            "working_hours": [working_hour.to_dict() for working_hour in self.working_hours],
            "unavailable_periods": [unavailable_period.to_dict() for unavailable_period in self.unavailable_periods],
            "is_active": self.is_active,
            "is_deleted": self.is_deleted,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class WorkingHour(BaseModel):
    __tablename__ = "working_hour"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    service_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('service.id'))
    day_of_week: Mapped[DayOfWeek] = mapped_column(SQLAlchemyEnum(DayOfWeek))
    start_time: Mapped[datetime.time] = mapped_column(Time)
    end_time: Mapped[datetime.time] = mapped_column(Time)

    service: Mapped["Service"] = relationship("Service", back_populates="working_hours")

    def to_dict(self):
        return {
            "id": self.id,
            "day_of_week": self.day_of_week.value if self.day_of_week else None,
            "start_time": str(self.start_time),
            "end_time": str(self.end_time),
        }


class UnavailablePeriod(BaseModel):
    __tablename__ = "unavailable_period"

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

    role_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("role.id"), nullable=True)

    appointments: Mapped[List["Appointment"]] = relationship(
        "Appointment", back_populates="user"
    )

    role: Mapped["Role"] = relationship("Role")

    groups: Mapped[List["Group"]] = relationship(
        secondary=group_user, back_populates="users"
    )

    own_groups: Mapped[List["Group"]] = relationship(
        "Group", back_populates="owner"
    )

    own_services: Mapped[List["Service"]] = relationship(
        "Service", back_populates="owner"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "name": self.name,
            "line_user_id": self.line_user_id,
            "phone": self.phone,
            "role": self.role.name.value if self.role else None,
            "is_active": self.is_active,
            "is_deleted": self.is_deleted,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "groups": [group.to_self_dict() for group in self.groups],
            "appointments": [appointment.to_dict() for appointment in self.appointments if not appointment.is_deleted],
        }
    
    def to_self_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "name": self.name,
            "line_user_id": self.line_user_id,
            "phone": self.phone,
            "role": self.role.name.value if self.role else None,
            "is_active": self.is_active,
            "is_deleted": self.is_deleted,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
    
    def to_auth(self):
        return {
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "password": self.password,
            "email": self.email,
            "role": self.role.name.value if self.role else None,
            "is_active": self.is_active,
        }


class Appointment(BaseModel, CommonColumns):
    __tablename__ = "appointment"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user_account.id"), nullable=False)
    service_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("service.id"), nullable=False)
    reserved_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="appointments")
    service: Mapped["Service"] = relationship("Service", back_populates="appointments")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "service_id": self.service_id,
            "reserved_at": self.reserved_at,
            "notes": self.notes,
            "is_active": self.is_active,
            "is_deleted": self.is_deleted,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "service": self.service.to_self_dict(),
        }
    

class Role(BaseModel):
    __tablename__ = "role"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[RoleName] = mapped_column(SQLAlchemyEnum(RoleName))


class Group(BaseModel, CommonColumns):
    __tablename__ = "line_group"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(Text)
    line_group_id: Mapped[str] = mapped_column(
        Text, unique=True, comment="Group Id For Line"
    )
    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user_account.id"))

    users: Mapped[List[User]] = relationship(
        secondary=group_user, back_populates="groups"
    )

    services: Mapped[List[Service]] = relationship(
        secondary=group_service, back_populates="groups"
    )

    owner: Mapped[User] = relationship("User", back_populates="own_groups")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "line_group_id": self.line_group_id,
            "is_active": self.is_active,
            "is_deleted": self.is_deleted,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "owner": self.owner.to_self_dict(),
            "users": [user.to_self_dict() for user in self.users if not user.is_deleted],
            "services": [service.to_self_dict() for service in self.services if not service.is_deleted]
        }
    
    def to_self_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "line_group_id": self.line_group_id,
            "is_active": self.is_active,
            "is_deleted": self.is_deleted,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }