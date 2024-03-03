from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import select, or_, func
from sqlalchemy.orm import joinedload
from werkzeug.exceptions import NotFound, Conflict
from app.db.connect import get_session
from app.db.models import User, Service, Appointment, Group


class AppointmentRepository:
    def insert_one(self, user_id: str, appointment_data: dict):
        try:
            with get_session() as session:
                user = session.query(User).filter(User.id == user_id).first()
                service_id = appointment_data.get("service_id")
                service = (
                    session.query(Service).filter(Service.id == service_id).first()
                )

                if user is None:
                    raise NotFound("User not found.")
                if service is None:
                    raise NotFound("Service not found.")

                appointment = Appointment(
                    user_id=user_id,
                    service_id=service_id,
                    reserved_at=appointment_data.get("reserved_at"),
                    notes=appointment_data.get("notes"),
                )
                user.appointments.append(appointment)
                session.commit()
                session.refresh(user)

                return appointment.with_user_service_dict()

        except IntegrityError:
            raise Conflict("Appointment already exists")
        except SQLAlchemyError as e:
            raise e

    def select_one_by_fields(self, appointment_id: str):
        with get_session() as session:
            appointment = (
                session.query(Appointment)
                .filter(Appointment.id == appointment_id)
                .first()
            )

            if appointment is None:
                raise NotFound("Appointment not found")

            return appointment.with_user_service_dict()

    def select_the_most_coming_appointment(self, user_id: str):
        with get_session() as session:
            appointment = (
                session.query(Appointment)
                .filter(Appointment.user_id == user_id)
                .filter(Appointment.reserved_at > func.now())
                .order_by(Appointment.reserved_at.asc())
                .first()
            )

            if appointment is None:
                raise NotFound("Appointment not found")

            return appointment.with_user_service_dict()

    def select_all_by_filter(
        self,
        page: int = 1,
        per_page: int = 10,
        user_id: str | None = None,
        sort_field: str | None = None,
        sort_order: str | None = None,
        query: str | None = None,
        service_owner_id: str | None = None,
    ):
        with get_session() as session:
            base_query = (
                select(Appointment)
                .join(Service, Appointment.service_id == Service.id)
                .join(User, Appointment.user_id == User.id)
                .options(joinedload(Appointment.service).joinedload(Service.owner))
                .filter(Appointment.is_deleted == False)
            )

            if user_id is not None:
                base_query = base_query.filter(Appointment.user_id == user_id)

            if service_owner_id is not None:
                base_query = base_query.filter(Service.owner_id == service_owner_id)

            if query is not None:
                query = f"%{query}%"
                base_query = base_query.filter(
                    or_(
                        Appointment.notes.ilike(query),
                        Service.name.ilike(query),
                        Service.owner.has(User.name.ilike(query)),
                        Service.groups.any(Group.name.ilike(query)),
                        User.name.ilike(query),
                    )
                )

            if sort_field is not None:
                sort_field = getattr(Appointment, sort_field)
                if sort_order == "ascend":
                    base_query = base_query.order_by(sort_field.asc())
                else:
                    base_query = base_query.order_by(sort_field.desc())

            base_query = base_query.offset((page - 1) * per_page).limit(per_page)
            appointments = session.scalars(base_query).all()
            return [appointment.with_user_service_dict() for appointment in appointments]

    def count_all_by_filter(
        self,
        user_id: str | None = None,
        service_owner_id: str | None = None,
        query: str | None = None,
    ):
        with get_session() as session:
            base_query = (
                select(func.count(Appointment.id))
                .join(Service, Appointment.service_id == Service.id)
                .join(User, Appointment.user_id == User.id)
                .filter(Appointment.is_deleted == False)
            )

            if user_id is not None:
                base_query = base_query.filter(Appointment.user_id == user_id)

            if service_owner_id is not None:
                base_query = base_query.filter(Service.owner_id == service_owner_id)

            if query is not None:
                query = f"%{query}%"
                base_query = base_query.filter(
                    or_(
                        Appointment.notes.ilike(query),
                        Service.name.ilike(query),
                        Service.owner.has(User.name.ilike(query)),
                        Service.groups.any(Group.name.ilike(query)),
                        User.name.ilike(query),
                    )
                )
            
            count_result = session.execute(base_query).scalar_one()
            return count_result

    def update_one(self, appointment_id: str, appointment_data: dict):
        with get_session() as session:
            appointment = (
                session.query(Appointment)
                .filter(Appointment.id == appointment_id)
                .first()
            )
            if appointment is None:
                raise NotFound("Appointment not found")

            for field, value in appointment_data.items():
                if value is not None:
                    setattr(appointment, field, value)

            session.commit()
            session.refresh(appointment)
            return appointment.with_user_service_dict()

    def delete_one(self, appointment_id: str):
        with get_session() as session:
            appointment = (
                session.query(Appointment)
                .filter(Appointment.id == appointment_id)
                .first()
            )
            if appointment is None:
                raise NotFound("Appointment not found")

            session.delete(appointment)
            session.commit()
