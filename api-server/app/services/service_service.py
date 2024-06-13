from typing import List, Tuple
from app.repositories import (
    ServiceRepository,
    WorkingHourRepository,
    UnavailablePeriodRepository,
    GroupRepository,
)
from app.db.models import DayOfWeek
from werkzeug.exceptions import BadRequest, NotFound, Forbidden
from datetime import datetime


class ServiceService:
    def __init__(self) -> None:
        self.service_repository = ServiceRepository()
        self.group_repository = GroupRepository()
        self.working_hour_repository = WorkingHourRepository()
        self.unavailable_period_repository = UnavailablePeriodRepository()

    def create_one(self, service_json_data: dict, payload: dict | None = {}) -> dict:
        working_hours = service_json_data.get("working_hours", []) or []
        unavailable_periods = service_json_data.get("unavailable_periods", []) or []
        group_ids = service_json_data.get("groups")
        user_id = payload.get("sub")
        role = payload.get("role")

        if user_id is None:
            raise BadRequest("sub must be provided in JWT payload")
        
        if group_ids is not None:
            is_user_owns_groups = self.group_repository.check_groups_owner_by_user_id(
                user_id=user_id, group_ids=group_ids
            )
            if role not in ["admin"] and not is_user_owns_groups:
                raise Forbidden("You are not the owner of one of the groups")

        # Validate working_hours
        days_of_week = set()
        for working_hour in working_hours:
            day_of_week = working_hour.get("day_of_week")
            if day_of_week in days_of_week:
                raise BadRequest("day_of_week cannot be duplicated")
            if day_of_week not in [day.value for day in DayOfWeek]:
                raise BadRequest(
                    "day_of_week must be one of Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday"
                )
            days_of_week.add(day_of_week)
            start_time = datetime.strptime(
                working_hour.get("start_time"), "%H:%M"
            ).time()
            end_time = datetime.strptime(working_hour.get("end_time"), "%H:%M").time()
            if start_time > end_time:
                raise BadRequest("start_time cannot be greater than end_time")

        # Validate unavailable_periods
        for unavailable_period in unavailable_periods:
            start_datetime = datetime.strptime(
                unavailable_period.get("start_datetime"), "%Y-%m-%d %H:%M:%S"
            )
            end_datetime = datetime.strptime(
                unavailable_period.get("end_datetime"), "%Y-%m-%d %H:%M:%S"
            )
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
        return self.service_repository.insert_one(
            new_service_data, working_hours, unavailable_periods, group_ids
        )

    def get_all(
        self,
        page: int = 1,
        per_page: int = 10,
        query: str = None,
        status: int = None,
        line_group_id: str = None,
        with_total_items: bool = False,
        payload: dict | None = {}
    ) -> List[dict] | Tuple[List[dict], int]:
        '''
        'group_owner' can only view services in their groups, identified by 'owner_id'.
        'line_bot' and 'liff' can only view services in their groups, identified by 'line_group_id'.
        'admin' can view all services.
        '''
        role = payload.get("role")
        owner_id = payload.get("sub") if role != "admin" else None
        group_id = self.__convert_line_group_id_to_group_id(line_group_id) if line_group_id else None
        services = self.service_repository.select_all_by_filter(
            page, per_page, query, status, owner_id, group_id
        )
        if with_total_items:
            total_items_count = self.service_repository.count_all_by_filter(
                query, status, owner_id, group_id
            )
            return services, total_items_count
        return services

    def get_most_popular_by_line_group_id(self, line_group_id: str, limit: int = 5) -> List[dict]:
        return self.service_repository.select_most_popular_by_line_group_id(line_group_id, limit)

    def get_one(self, service_id: str, payload: dict | None = {}) -> dict:
        role = payload.get("role")
        if role in ["liff", "line_bot", "admin"]:
            return self.service_repository.select_one_by_unique_filed(
                service_id=service_id
            )

        user_id = payload.get("sub")

        if role in ["group_member"]:
            is_user_in_group = self.service_repository.check_if_user_in_group_by_service_id(
                service_id=service_id, user_id=user_id
            )
            if not is_user_in_group:
                raise Forbidden("You are not in the group of this service")
            
        if role in ["group_owner"]:
            is_user_own_service = self.service_repository.check_if_user_own_service(
                service_id=service_id, user_id=user_id
            )
            if not is_user_own_service:
                raise Forbidden("You are not the owner of service")

        return self.service_repository.select_one_by_unique_filed(
            service_id=service_id
        )

    def delete_one(self, service_id: str, payload: dict | None = {}) -> dict:
        user_id = payload.get("sub")
        role = payload.get("role")

        is_user_own_service = self.service_repository.check_if_user_own_service(
            service_id=service_id, user_id=user_id
        )

        if role not in ["admin"] and not is_user_own_service:
            raise Forbidden("You are not the owner of service")

        return self.service_repository.logical_delete_one_by_id(service_id)

    def update_one(self, service_id: str, service_json_data: dict, payload: dict | None = {}) -> dict:
        user_id = payload.get("sub")
        role = payload.get("role")

        is_user_own_service = self.service_repository.check_if_user_own_service(
            service_id=service_id, user_id=user_id
        )
        if role not in ["admin"] and not is_user_own_service:
            raise Forbidden("You are not the owner of service")

        input_unavailable_periods = service_json_data.get("unavailable_periods")
        input_working_hours = service_json_data.get("working_hours")
        group_ids = service_json_data.get("groups")

        update_service_data = {
            "name": service_json_data.get("name"),
            "price": service_json_data.get("price"),
            "image": service_json_data.get("image"),
            "description": service_json_data.get("description"),
            "working_period": service_json_data.get("working_period"),
            "is_active": service_json_data.get("is_active"),
        }
        return self.service_repository.update_one_by_id(
            service_id,
            update_service_data,
            group_ids,
            input_working_hours,
        )

    def __convert_line_group_id_to_group_id(self, line_group_id: str):
        group_data = self.group_repository.select_one_by_unique_filed(
            line_group_id=line_group_id
        )
        return group_data.get("id")
