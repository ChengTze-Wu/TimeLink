from web_api.db.models import User, Service
from werkzeug.exceptions import NotFound, BadRequest
from datetime import datetime
from sqlalchemy.orm import Session


def validate_appointment_data(session: Session, user_id, service_id, appointment_datetime):
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise NotFound("User not found")

    service = session.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise NotFound("Service not found")

    if not set(user.groups).intersection(set(service.groups)):
        raise NotFound(f"User `{user.name}` is not in service `{service.name}` group")

    if not service.is_active:
        raise BadRequest(f"Service `{service.name}` is not active")

    if not service.open_time <= datetime.now().time() <= service.close_time:
        raise BadRequest(f"Service `{service.name}` is not open")

    for unavailable_period in service.unavailable_periods:
        if (
            unavailable_period.start_datetime
            <= datetime.now()
            <= unavailable_period.end_datetime
        ):
            raise BadRequest(f"Service `{service.name}` is not available")

    if appointment_datetime < datetime.now():
        raise BadRequest("Appointment time must be greater than now")

    appointment_data, appointment_time = appointment_datetime.split(" ")

    if appointment_data < service.start_date or appointment_data > service.end_date:
        raise BadRequest(f"Service `{service.name}` is not available")

    if appointment_time < service.open_time or appointment_time > service.close_time:
        raise BadRequest(f"Service `{service.name}` is not available")

    if (appointment_time - service.open_time) % service.period_time != 0:
        raise BadRequest(f"Service `{service.name}` is not available")
