from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import select, or_
from werkzeug.exceptions import NotFound, Conflict
from app.db.connect import get_session
from app.db.models import User, Service, Appointment


class AppointmentRepository:
    def insert_one(self, user_id: str, appointment_data: dict):
        try:
            with get_session() as session:
                user = session.query(User).filter(User.id == user_id).first()
                service_id = appointment_data.get("service_id")
                service = session.query(Service).filter(Service.id == service_id).first()

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
        
    def update_one(self, appointment_id: str, appointment_data: dict):
        with get_session() as session:
            appointment = session.query(Appointment).filter(Appointment.id == appointment_id).first()
            if appointment is None:
                raise NotFound("Appointment not found")

            for field, value in appointment_data.items():
                if value is not None:
                    setattr(appointment, field, value)

            session.commit()
            session.refresh(appointment)
            return appointment.to_dict()