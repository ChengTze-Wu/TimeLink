from typing import List, Tuple
from web_api.repositories.group_repository import GroupRepository


class GroupService:
    def __init__(self):
        self.group_repository = GroupRepository()

    def create_one(self, group_json_data: dict) -> dict:
        new_group_data = {
            "id": group_json_data.get("id"),
            "name": group_json_data.get("name"),
            "line_group_id": group_json_data.get("line_group_id"),
            "is_active": group_json_data.get("is_active", True),
            "is_deleted": group_json_data.get("is_deleted", False),
        }
        return self.group_repository.create_one(new_group_data)

    def update_one(self, group_id: str, group_json_data: dict) -> dict:
        update_group_data = {
            "name": group_json_data.get("name"),
            "line_group_id": group_json_data.get("line_group_id"),
            "is_active": group_json_data.get("is_active"),
            "is_deleted": group_json_data.get("is_deleted"),
        }
        return self.group_repository.update_one_by_id(group_id, update_group_data)

    def delete_one(self, group_id: str) -> dict:
        return self.group_repository.logical_delete_one_by_id(group_id)

    def get_one(self, group_id: str) -> dict:
        return self.group_repository.get_one_by_unique_filed(group_id=group_id)

    def get_all(
        self,
        page: int = 1,
        per_page: int = 10,
        query: str = None,
        status: int = None,
        with_total_items: bool = False,
    ) -> List[dict] | Tuple[List[dict], int]:
        list_dict_groups = self.group_repository.get_all_by_filter(
            page, per_page, query, status
        )
        if with_total_items:
            total_items_count = self.group_repository.count_all_by_filter(query, status)
            return list_dict_groups, total_items_count

        return list_dict_groups
