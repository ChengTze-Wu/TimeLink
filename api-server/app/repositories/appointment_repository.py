from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import select, or_, and_
from werkzeug.exceptions import NotFound, Conflict
from app.db.connect import get_session
from app.db.models import User, Service, Appointment


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

                return appointment.to_dict()

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

            return appointment.to_dict()

    def select_all_by_filter_and_paganation(
        self,
        page: int,
        per_page: int,
        user_id: str | None = None,
        service_id: str | None = None,
    ):
        with get_session() as session:
            appointments = (
                session.query(Appointment)
                .filter(
                    or_(
                        Appointment.user_id == user_id,
                        Appointment.service_id == service_id,
                    )
                )
                .offset((page - 1) * per_page)
                .limit(per_page)
                .all()
            )

            return [appointment.to_dict() for appointment in appointments]

    def select_all_by_filter(
        self,
        page: int = 1,
        per_page: int = 10,
        user_id: str | None = None,
        service_id: str | None = None,
    ):
        with get_session() as session:
            base_query = (
                select(Appointment)
                .filter(
                    or_(
                        Appointment.user_id == user_id,
                        Appointment.service_id == service_id,
                    )
                )
                .order_by(Appointment.created_at.desc())
            )
            base_query = base_query.offset((page - 1) * per_page).limit(per_page)
            appointments = session.scalars(base_query).all()
            return [appointment.to_dict() for appointment in appointments]

    def count_all_by_filter(
        self, user_id: str | None = None, service_id: str | None = None
    ):
        return len(self.select_all_by_filter(user_id=user_id, service_id=service_id))

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
            return appointment.to_dict()

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
