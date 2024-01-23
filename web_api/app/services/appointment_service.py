from app.repositories.appointment_repository import AppointmentRepository
from app.repositories.service_repository import ServiceRepository
from typing import List, Tuple
from datetime import datetime, timedelta
from werkzeug.exceptions import NotFound, BadRequest

'''
服務會隸屬於某個群組，群組


'''

class AppointmentService:
    def __init__(self):
        self.appointment_repository = AppointmentRepository()
        self.service_repository = ServiceRepository()

    def create_one(self, user_id: str, appointment_json_data: dict) -> dict:
        service_id = appointment_json_data.get("service_id")
        reserved_at = appointment_json_data.get("reserved_at")

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
        service_id = appointment_json_data.get("service_id")
        reserved_at = appointment_json_data.get("reserved_at")

        self.__check_service_availability(service_id, reserved_at)

        return self.appointment_repository.update_one(
            appointment_id=appointment_id, 
            appointment_data={
                "reserved_at": appointment_json_data.get("reserved_at"),
                "notes": appointment_json_data.get("notes"),
            },
        )
    

    def cancel_one(self, appointment_id: str) -> dict:
        return self.appointment_repository.delete_one(appointment_id=appointment_id)
    

    def get_one(self, appointment_id: str) -> dict:
        appointment_data = self.appointment_repository.select_one(appointment_id=appointment_id)
        if appointment_data is None:
            raise NotFound("Appointment not found")
        return appointment_data
    

    def get_all(
        self,
        page: int = 1,
        per_page: int = 10,
        query: str = None,
        reserved_at: str = None,
        user_id: str = None,
        service_id: str = None,
        is_active: bool = True,
    ) -> Tuple[List[dict], int]:
        return self.appointment_repository.select_all(
            page=page,
            per_page=per_page,
            query=query,
            reserved_at=reserved_at,
            user_id=user_id,
            service_id=service_id,
            is_active=is_active,
        )

    
    def __check_service_availability(self, service_id: str, reserved_at: str) -> bool:
        weekday_mapping = {
            0: "Monday",
            1: "Tuesday",
            2: "Wednesday",
            3: "Thursday",
            4: "Friday",
            5: "Saturday",
            6: "Sunday",
        }

        service_data = self.service_repository.select_one_by_unique_filed(service_id=service_id)
        working_hours = service_data.get("working_hours")
        working_period = service_data.get("working_period")

        reserved_datetime = datetime.strptime(reserved_at, "%Y-%m-%d %H:%M:%S")
        reserved_finish_datetime = reserved_datetime + timedelta(minutes=working_period)
        reserved_time = reserved_datetime.time()
        reserved_finish_time = reserved_finish_datetime.time()
        reserved_weekday = weekday_mapping.get(reserved_datetime.weekday())

        working_days = set()
        for working_hour in working_hours:
            working_days.add(working_hour.get("day_of_week"))
            if working_hour.get("day_of_week") == reserved_weekday:
                start_time = datetime.strptime(working_hour.get("start_time"), "%H:%M:%S").time()
                end_time = datetime.strptime(working_hour.get("end_time"), "%H:%M:%S").time()
                if not start_time <= reserved_time < end_time or not start_time < reserved_finish_time <= end_time:
                    raise BadRequest(f"Invalid reserved time. The service is only available from {start_time} to {end_time} on {reserved_weekday}")       
                break
        else:
            raise BadRequest(f"Invalid reserved time. The service is only available on {working_days}")
        
        return True