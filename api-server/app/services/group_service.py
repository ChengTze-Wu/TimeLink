import os
import requests
from werkzeug.exceptions import NotFound, BadRequest, Forbidden
from typing import List, Tuple
from app.repositories import GroupRepository


CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")
if CHANNEL_ACCESS_TOKEN is None:
    raise ValueError("CHANNEL_ACCESS_TOKEN Environment Variable is not set")


class GroupService:
    def __init__(self):
        self.group_repository = GroupRepository()

    def create_one(self, group_json_data: dict, payload: dict | None = {}) -> dict:
        line_group_id = group_json_data.get("line_group_id")
        line_group_summary = self.__fetch_group_summary_from_lineapi(line_group_id)
        user_id = payload.get("sub")

        if user_id is None:
            raise BadRequest("sub must be provided in JWT payload")

        new_group_data = {
            "name": line_group_summary.get("groupName"),
            "line_group_id": line_group_id,
            "is_active": group_json_data.get("is_active", True),
            "owner_id": user_id,
        }
        return self.group_repository.insert_one(new_group_data)

    def get_one(self, group_id: str = None, line_group_id: str = None, payload: dict | None = {}) -> dict:
        if group_id:
            return self.__retrieve_group_by_owner(group_id, payload)

        if line_group_id:
            return self.group_repository.select_one_by_unique_filed(
                line_group_id=line_group_id
            )

        raise BadRequest("group_id or line_group_id must be provided")

    def get_all(
        self,
        page: int = 1,
        per_page: int = 10,
        query: str = None,
        status: int = None,
        service_id: str = None,
        with_total_items: bool = False,
        payload: dict | None = {},
    ) -> List[dict] | Tuple[List[dict], int]:
        role = payload.get("role")
        owner_id = payload.get("sub") if role != "admin" else None
        list_dict_groups = self.group_repository.select_all_by_filter(
            page, per_page, query, status, owner_id, service_id=service_id, with_by="owner"
        )
        if with_total_items:
            total_items_count = self.group_repository.count_all_by_filter(
                query, status, owner_id
            )
            return list_dict_groups, total_items_count

        return list_dict_groups

    def update_one(self, group_id: str, group_json_data: dict, payload: dict | None = {}) -> dict:
        self.__retrieve_group_by_owner(group_id, payload)
        update_group_data = {
            "is_active": group_json_data.get("is_active"),
        }
        return self.group_repository.update_one_by_id(group_id, update_group_data)

    def delete_one(self, group_id: str, payload: dict | None = {}) -> dict:
        self.__retrieve_group_by_owner(group_id, payload)
        return self.group_repository.logical_delete_one_by_id(group_id)

    def link_user_to_group(self, line_group_id: str, line_user_id: str) -> dict:
        return self.group_repository.add_user_to_group_by_line_ids(
            line_group_id, line_user_id
        )

    def unlink_user_from_group(self, line_group_id: str, line_user_id: str) -> dict:
        return self.group_repository.remove_user_from_group_by_line_ids(
            line_group_id, line_user_id
        )

    def __retrieve_group_by_owner(self, group_id: str, payload: dict | None = {}):
        role = payload.get("role")
        group_data = self.group_repository.select_one_by_unique_filed(group_id=group_id)
        if role != "admin" and payload.get("sub") != str(
            group_data.get("owner").get("id")
        ):
            raise Forbidden("You are not the owner of this group")
        return group_data

    def __fetch_group_summary_from_lineapi(self, line_group_id: str) -> dict:
        line_api_endpoint = f"https://api.line.me/v2/bot/group/{line_group_id}/summary"
        headers = {
            "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}",
        }
        response = requests.get(line_api_endpoint, headers=headers, timeout=3)
        if response.status_code == 400:
            raise BadRequest(response.json()["message"])
        elif response.status_code == 404:
            raise NotFound(response.json()["message"])
        response.raise_for_status()
        return response.json()
