from typing import List, Tuple
from web_api.repositories.service_repository import ServiceRepository
from werkzeug.exceptions import BadRequest


class ServiceService:
    def __init__(self) -> None:
        self.service_repository = ServiceRepository()

    def create_one(self, service_json_data: dict) -> dict:
        '''
        service_json_data example:
        {
            "name": "string",
            "price": 0,
            "image": "path/to/image",
            "description": "string",
            "working_hours": [
                {
                    "day_of_week": "Monday",
                    "start_time": "09:00",
                    "end_time": "18:00"
                }
            ],
            "unavailable_periods": [
                {
                    "start_datetime": "2023-12-11 08:12:00",
                    "end_datetime": "2023-12-11 09:12:00"
                }
            ]
        }
        '''
        working_hours = service_json_data.get("working_hours", [])
        unavailable_periods = service_json_data.get("unavailable_periods", [])

        for working_hour in working_hours:
            if working_hour.get("open_time") > working_hour.get("close_time"):
                raise BadRequest("open_time cannot be greater than close_time")
        for unavailable_period in unavailable_periods:
            if unavailable_period.get("start_datetime") > unavailable_period.get("end_datetime"):
                raise BadRequest("start_datetime cannot be greater than end_datetime")
            
        new_service_data = {
            "name": service_json_data.get("name"),
            "price": service_json_data.get("price"),
            "image": service_json_data.get("image"),
            "description": service_json_data.get("description"),
            "working_hours": working_hours,
            "unavailable_periods": unavailable_periods
        }
            
        return self.service_repository.create_one(new_service_data)


    def delete_one(self, service_id: str) -> dict:
        return self.service_repository.logical_delete_one_by_id(service_id)


    def update_one(self, service_id: str, service_data: dict) -> dict:
        working_hours = service_data.get("working_hours", [])
        unavailable_periods = service_data.get("unavailable_periods", [])

        for working_hour in working_hours:
            if working_hour.get("open_time") > working_hour.get("close_time"):
                raise BadRequest("open_time cannot be greater than close_time")
        for unavailable_period in unavailable_periods:
            if unavailable_period.get("start_datetime") > unavailable_period.get("end_datetime"):
                raise BadRequest("start_datetime cannot be greater than end_datetime")
            
        update_service_data = {
            "name": service_data.get("name"),
            "price": service_data.get("price"),
            "image": service_data.get("image"),
            "description": service_data.get("description"),
            "working_hours": working_hours,
            "unavailable_periods": unavailable_periods
        }

        return self.service_repository.update_one_by_id(service_id, update_service_data)


    def get_one(self, service_id: str) -> dict:
        return self.service_repository.get_one_by_unique_filed(service_id=service_id)


    def get_all(
        self,
        page: int = 1,
        per_page: int = 10,
        query: str = None,
        status: int = None,
        with_total_items: bool = False,
    ) -> List[dict] | Tuple[List[dict], int]:
        list_dict_services = self.service_repository.get_all_by_filter(
            page, per_page, query, status
        )
        if with_total_items:
            total_items_count = self.service_repository.count_all_by_filter(query, status)
            return list_dict_services, total_items_count
        return list_dict_services
