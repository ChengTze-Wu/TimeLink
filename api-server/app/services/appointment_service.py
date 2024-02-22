from datetime import datetime, timedelta
from werkzeug.exceptions import BadRequest, Forbidden
from app.db.models import RoleName
from .token_service import JWTService
from app.repositories import (
    AppointmentRepository,
    ServiceRepository,
    UserRepository,
    GroupRepository,
)


class AppointmentService:
    def __init__(self):
        self.appointment_repository = AppointmentRepository()
        self.service_repository = ServiceRepository()
        self.user_repository = UserRepository()
        self.group_repository = GroupRepository()
        self.payload = JWTService().get_payload()

    def create_one(self, appointment_json_data: dict) -> dict:
        """Create an appointment by self For LIFF."""
        service_id = appointment_json_data.get("service_id")
        reserved_at = appointment_json_data.get("reserved_at")
        line_user_id = appointment_json_data.get("line_user_id")
        user_id = (
            self.__convert_line_user_id_to_user_id(line_user_id)
            if line_user_id
            else self.payload.get("sub")
        )

        if user_id is None:
            raise BadRequest(
                "user_id must be provided in JWT sub or line_user_id be provided in request body"
            )

        self.__check_service_availability(service_id, reserved_at)

        return self.appointment_repository.insert_one(
            user_id=user_id,
            appointment_data={
                "service_id": service_id,
                "reserved_at": reserved_at,
                "notes": appointment_json_data.get("notes"),
            },
        )

    def update_one(self, appointment_id: str, appointment_json_data: dict) -> dict:
        reserved_at = appointment_json_data.get("reserved_at")
        is_active = appointment_json_data.get("is_active")
        line_user_id = appointment_json_data.get("line_user_id")
        user_id = (
            self.payload.get("sub")
            if self.payload.get("sub")
            else self.__convert_line_user_id_to_user_id(line_user_id)
        )
        role = self.payload.get("role")

        if user_id is None:
            raise BadRequest(
                "user_id must be provided in JWT sub or line_user_id be provided in request body"
            )

        appointment = self.appointment_repository.select_one_by_fields(
            appointment_id=appointment_id
        )
        service_id = appointment.get("service_id")

        self.__check_service_availability(service_id, reserved_at)

        if role == RoleName.GROUP_OWNER.value:
            self.__check_appointment_belongs_owner_groups(appointment_id, user_id)

        if role not in [RoleName.ADMIN.value, RoleName.GROUP_OWNER.value]:
            self.__check_apointment_belongs_user(appointment_id, user_id)

        return self.appointment_repository.update_one(
            appointment_id=appointment_id,
            appointment_data={
                "reserved_at": reserved_at,
                "notes": appointment_json_data.get("notes"),
                "is_active": is_active,
            },
        )

    def cancel_one(self, appointment_id: str, line_user_id: str | None = None) -> dict:
        """Cancel an appointment by deleting it. The appointment will
        be removed from the database.
        """
        user_id = (
            self.payload.get("sub")
            if self.payload.get("sub")
            else self.__convert_line_user_id_to_user_id(line_user_id)
        )
        role = self.payload.get("role")

        if user_id is None:
            raise BadRequest(
                "user_id must be provided in JWT sub or be provided line_user_id in query string"
            )

        if role == RoleName.GROUP_OWNER.value:
            self.__check_appointment_belongs_owner_groups(appointment_id, user_id)

        if role not in [RoleName.ADMIN.value, RoleName.GROUP_OWNER.value]:
            self.__check_apointment_belongs_user(appointment_id, user_id)

        return self.appointment_repository.delete_one(appointment_id=appointment_id)

    def get_one(self, appointment_id: str) -> dict:
        """For Web App"""
        user_id = self.payload.get("sub")
        role = self.payload.get("role")

        if role == RoleName.GROUP_OWNER.value:
            self.__check_appointment_belongs_owner_groups(appointment_id, user_id)

        if role not in [RoleName.ADMIN.value, RoleName.GROUP_OWNER.value]:
            self.__check_apointment_belongs_user(appointment_id, user_id)

        return self.appointment_repository.select_one_by_fields(
            appointment_id=appointment_id
        )

    def get_all(
        self,
        page: int = 1,
        per_page: int = 10,
        line_user_id: str | None = None,
        service_id: str | None = None,
        with_total_count: bool = False,
    ) -> tuple[list[dict], int] | list[dict]:
        user_id = (
            self.payload.get("sub")
            if self.payload.get("sub")
            else self.__convert_line_user_id_to_user_id(line_user_id)
        )
        role = self.payload.get("role")

        if user_id is None:
            raise BadRequest(
                "user_id must be provided in JWT sub or be provided line_user_id in query string"
            )

        if role == RoleName.GROUP_OWNER.value:
            appointments = self.appointment_repository.select_all_by_filter(
                page=page, per_page=per_page, service_id=service_id, service_owner_id=user_id
            )
            if with_total_count:
                total_count = self.appointment_repository.count_all_by_filter(
                    service_id=service_id, service_owner_id=user_id
                )
                return appointments, total_count
        elif role == RoleName.ADMIN.value:
            appointments = self.appointment_repository.select_all_by_filter(
                page=page, per_page=per_page, service_id=service_id
            )
            if with_total_count:
                total_count = self.appointment_repository.count_all_by_filter(
                    service_id=service_id
                )
                return appointments, total_count
        else:
            appointments = self.appointment_repository.select_all_by_filter(
                page=page, per_page=per_page, user_id=user_id, service_id=service_id
            )

        if with_total_count:
            return appointments, self.appointment_repository.count_all_by_filter(
                user_id=user_id, service_id=service_id
            )
        return appointments

    def __check_service_availability(self, service_id: str, reserved_at: str):
        """Check if the service is available at the reserved time, considering
        the working hours and working period of the service.
        """
        weekday_mapping = {
            0: "Monday",
            1: "Tuesday",
            2: "Wednesday",
            3: "Thursday",
            4: "Friday",
            5: "Saturday",
            6: "Sunday",
        }

        service_data = self.service_repository.select_one_by_unique_filed(
            service_id=service_id
        )
        working_hours = service_data.get("working_hours")  # 該服務每日營業時間
        working_period = service_data.get("working_period")  # 該服務每次服務時間

        if working_hours is None or working_period is None:
            raise BadRequest(
                "The service does not have working hours or working period, please contact the owner"
            )

        reserved_datetime = datetime.strptime(reserved_at, "%Y-%m-%d %H:%M:%S")
        reserved_finish_datetime = reserved_datetime + timedelta(minutes=working_period)
        reserved_time = reserved_datetime.time()
        reserved_finish_time = reserved_finish_datetime.time()  # 預約經過服務時間後的結束時間
        reserved_weekday = weekday_mapping.get(reserved_datetime.weekday())
        working_days = set()
        for working_hour in working_hours:
            working_days.add(working_hour.get("day_of_week"))
            if working_hour.get("day_of_week") == reserved_weekday:
                start_time = datetime.strptime(
                    working_hour.get("start_time"), "%H:%M:%S"
                ).time()
                end_time = datetime.strptime(
                    working_hour.get("end_time"), "%H:%M:%S"
                ).time()
                if not start_time <= reserved_time < end_time:
                    raise BadRequest(
                        f"Invalid reserved time. The service is only available from {start_time} to {end_time} on {reserved_weekday}"
                    )
                if not start_time < reserved_finish_time <= end_time:
                    raise BadRequest(
                        f"Invalid reserved time. Your reserved finish time is {reserved_finish_time}. The service is only available from {start_time} to {end_time} on {reserved_weekday}"
                    )
                break
        else:
            raise BadRequest(
                f"Invalid reserved time. The service is only available on {working_days}"
            )

    def __check_appointment_belongs_owner_groups(
        self, appointment_id: str, owner_id: str
    ):
        group = self.group_repository.select_one_by_unique_filed(owner_id=owner_id)
        appointment = self.appointment_repository.select_one_by_fields(
            appointment_id=appointment_id
        )
        services: list[dict] = group.get("services")
        for service in services:
            if service.get("id") == appointment.get("service_id"):
                return
        raise Forbidden("Appointment does not belong to owner's group")

    def __check_apointment_belongs_user(self, appointment_id: str, user_id: str):
        appointment = self.appointment_repository.select_one_by_fields(
            appointment_id=appointment_id
        )
        if appointment.get("user_id") == user_id:
            return
        raise Forbidden("Appointment does not belong to user")

    def __convert_line_user_id_to_user_id(self, line_user_id: str) -> str:
        user_data = self.user_repository.select_one_by_unique_filed(
            line_user_id=line_user_id
        )
        return user_data.get("id")
