from typing import List, Tuple
from app.repositories import (
    ServiceRepository,
    WorkingHourRepository,
    UnavailablePeriodRepository,
    GroupRepository,
)
from .token_service import JWTService
from app.db.models import DayOfWeek
from werkzeug.exceptions import BadRequest
from datetime import datetime
from uuid import UUID


class ServiceService:
    def __init__(self) -> None:
        self.service_repository = ServiceRepository()
        self.group_repository = GroupRepository()
        self.working_hour_repository = WorkingHourRepository()
        self.unavailable_period_repository = UnavailablePeriodRepository()
        self.payload = JWTService().get_payload()

    def create_one(self, service_json_data: dict) -> dict:
        working_hours = service_json_data.get("working_hours", []) or []
        unavailable_periods = service_json_data.get("unavailable_periods", []) or []
        group_ids = service_json_data.get("groups")
        user_id = self.payload.get("sub")

        if user_id is None:
            raise BadRequest("sub must be provided in JWT payload")

        # Validate working_hours
        days_of_week = set()
        for working_hour in working_hours:
            day_of_week = working_hour.get("day_of_week")
            if day_of_week in days_of_week:
                raise BadRequest("day_of_week cannot be duplicated")
            if day_of_week not in [day.value for day in DayOfWeek]:
                raise BadRequest("day_of_week must be one of Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday")
            days_of_week.add(day_of_week)
            start_time = datetime.strptime(working_hour.get("start_time"), "%H:%M").time()
            end_time = datetime.strptime(working_hour.get("end_time"), "%H:%M").time()
            if start_time > end_time:
                raise BadRequest("start_time cannot be greater than end_time")
            
        # Validate unavailable_periods
        for unavailable_period in unavailable_periods:
            start_datetime = datetime.strptime(unavailable_period.get("start_datetime"), "%Y-%m-%d %H:%M:%S")
            end_datetime = datetime.strptime(unavailable_period.get("end_datetime"), "%Y-%m-%d %H:%M:%S")
            if start_datetime > end_datetime:
                raise BadRequest("start_datetime cannot be greater than end_datetime")
            
        new_service_data = {
            "name": service_json_data.get("name"),
            "price": service_json_data.get("price"),
            "image": service_json_data.get("image"),
            "description": service_json_data.get("description"),
            "working_period": service_json_data.get("working_period"),
            "is_active": service_json_data.get("is_active"),
            "owner_id": user_id,
        }
        return self.service_repository.insert_one(new_service_data, working_hours, unavailable_periods, group_ids)

    def get_all(
        self,
        page: int = 1,
        per_page: int = 10,
        query: str = None,
        status: int = None,
        with_total_items: bool = False,
    ) -> List[dict] | Tuple[List[dict], int]:
        role = self.payload.get("role")
        owner_id = self.payload.get("sub") if role != "admin" else None
        services = self.service_repository.select_all_by_filter(
            page, per_page, query, status, owner_id
        )
        if with_total_items:
            total_items_count = self.service_repository.count_all_by_filter(query, status, owner_id)
            return services, total_items_count
        return services

    def get_one(self, service_id: str) -> dict:
        return self.__retrieve_service_by_owner(service_id)

    def delete_one(self, service_id: str) -> dict:
        self.__retrieve_service_by_owner(service_id)
        return self.service_repository.logical_delete_one_by_id(service_id)

    def update_one(self, service_id: str, service_json_data: dict) -> dict:
        self.__retrieve_service_by_owner(service_id)

        input_unavailable_periods = service_json_data.get("unavailable_periods", [])
        input_working_hours = service_json_data.get("working_hours", [])
        group_ids = service_json_data.get("groups")

        update_service_data = {
            "name": service_json_data.get("name"),
            "price": service_json_data.get("price"),
            "image": service_json_data.get("image"),
            "description": service_json_data.get("description"),
            "working_period": service_json_data.get("working_period"),
            "is_active": service_json_data.get("is_active")
        }
        return self.service_repository.update_one_by_id(
            service_id, 
            update_service_data,
            group_ids,
            input_working_hours,
        )

    def __retrieve_service_by_owner(self, service_id: str):
        role = self.payload.get("role")
        service_data = self.service_repository.select_one_by_unique_filed(service_id=service_id)
        if role != "admin" and self.payload.get("sub") != str( service_data.get("owner").get("id")):
            raise BadRequest("You are not the owner of this service")
        return service_data