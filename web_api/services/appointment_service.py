from repositories.appointment_repository import AppointmentRepository
from validators.appointment_validator import validate_appointment_data
from werkzeug.exceptions import NotFound, BadRequest, Conflict

class AppointmentService:
    def __init__(self):
        self.repository = AppointmentRepository()

    def create_appointment(self, user_id, service_id, appointment_datetime):
        with self.repository.get_session() as session:
            validate_appointment_data(session, user_id, service_id, appointment_datetime)

            if self.repository.check_existing_appointment(session, service_id, user_id, appointment_datetime):
                raise Conflict("Appointment at this time already exists.")

            return self.repository.create_new_appointment(session, user_id, service_id, appointment_datetime)

