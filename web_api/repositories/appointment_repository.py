from web_api.db.connect import Session as connect_Session
from web_api.db.models import service_user, User, Service
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
from sqlalchemy.orm import Session


class AppointmentRepository:
    @contextmanager
    def get_session(self):
        session = connect_Session()
        try:
            yield session
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def check_existing_appointment(
        self, session: Session, service_id, user_id, appointment_datetime
    ):
        return (
            session.query(service_user)
            .filter(
                service_user.c.service_id == service_id,
                service_user.c.user_id == user_id,
                service_user.c.reserved_at == appointment_datetime,
            )
            .first()
            is not None
        )

    def create_new_appointment(
        self, session: Session, user_id, service_id, appointment_datetime
    ):
        new_appointment = service_user.insert().values(
            user_id=user_id, service_id=service_id, reserved_at=appointment_datetime
        )
        session.execute(new_appointment)
        session.flush()

        user = session.query(User).filter(User.id == user_id).first()
        service = session.query(Service).filter(Service.id == service_id).first()

        return {
            "user": user.to_dict(),
            "service": service.to_dict(),
            "reserved_at": appointment_datetime,
        }
