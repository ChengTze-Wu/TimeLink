from werkzeug.security import generate_password_hash
from web_api.repositories.user_repository import UserRepository
from typing import List, Tuple


class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def create(self, user_json_data: dict) -> dict:
        new_user_data = {
            "id": user_json_data.get("id"),
            "email": user_json_data.get("email"),
            "username": user_json_data.get("username"),
            "password": generate_password_hash(user_json_data.get("password")),
            "name": user_json_data.get("name"),
            "line_user_id": user_json_data.get("line_user_id"),
            "phone": user_json_data.get("phone"),
            "is_active": user_json_data.get("is_active", True),
            "is_deleted": user_json_data.get("is_deleted", False),
        }
        return self.repository.create_new_user(new_user_data)

    def update(self, user_id: str, user_json_data: dict) -> dict:
        update_user_data = {
            "email": user_json_data.get("email"),
            "username": user_json_data.get("username"),
            "password": generate_password_hash(user_json_data.get("password"))
            if user_json_data.get("password")
            else None,
            "name": user_json_data.get("name"),
            "line_user_id": user_json_data.get("line_user_id"),
            "phone": user_json_data.get("phone"),
            "is_active": user_json_data.get("is_active"),
            "is_deleted": user_json_data.get("is_deleted"),
        }
        return self.repository.update_user_by_id(user_id, update_user_data)

    def delete(self, user_id: str) -> dict:
        return self.repository.logical_delete_user_by_id(user_id)

    def get_one(self, user_id: str) -> dict:
        return self.repository.get_one_by_id(user_id)

    def get_list(
        self, page: int, per_page: int, query: str, status: int, with_total_items: bool
    ) -> List[dict] | Tuple[List[dict], int]:
        list_dict_users = self.repository.get_users_by_filter(
            page, per_page, query, status
        )
        if with_total_items:
            total_items_count = self.repository.count_all_users_by_filter(query, status)
            return list_dict_users, total_items_count
        return list_dict_users
