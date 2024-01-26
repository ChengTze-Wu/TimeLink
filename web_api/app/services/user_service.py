from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import NotFound, Forbidden, Unauthorized
from app.repositories import UserRepository
from typing import List, Tuple
from app.db.models import RoleName
from werkzeug.exceptions import BadRequest
from .token_service import JWTService


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()
        self.jwt_service = JWTService()

    def create_one(self, user_json_data: dict) -> dict:
        jwt_payload = self.jwt_service.get_payload()
        client_role = jwt_payload.get("role")
        create_role = user_json_data.get("role")

        if client_role != RoleName.ADMIN.value and create_role == RoleName.ADMIN.value:
            raise Forbidden("Only admin can select admin")

        if create_role is not None and create_role.lower() not in [create_role.value for create_role in RoleName]:
            raise BadRequest("Role must be one of admin, group_owner, group_member")

        new_user_data = {
            "email": user_json_data.get("email"),
            "username": user_json_data.get("username"),
            "password": generate_password_hash(user_json_data.get("password")),
            "name": user_json_data.get("name"),
            "line_user_id": user_json_data.get("line_user_id"),
            "phone": user_json_data.get("phone"),
            "is_active": user_json_data.get("is_active", True),
        }
        return self.user_repository.insert_one(new_user_data, create_role.upper() if create_role is not None else None)

    def update_one(self, user_id: str, user_json_data: dict) -> dict:
        jwt_payload = self.jwt_service.get_payload()
        create_role = user_json_data.get("role")
        client_role = jwt_payload.get("role")

        if client_role != RoleName.ADMIN.value and create_role == RoleName.ADMIN.value:
            raise Forbidden("Only admin can select admin")

        if create_role is not None and create_role.lower() not in [create_role.value for create_role in RoleName]:
            raise BadRequest("Role must be one of admin, group_owner, group_member")
        
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
        return self.user_repository.update_one_by_id(user_id, update_user_data, create_role.upper() if create_role is not None else None)

    def delete_one(self, user_id: str) -> dict:
        return self.user_repository.logical_delete_one_by_id(user_id)

    def get_one(self, user_id: str=None, line_user_id: str=None) -> dict:
        if user_id:
            return self.user_repository.select_one_by_unique_filed(user_id=user_id)
        if line_user_id:
            return self.user_repository.select_one_by_unique_filed(line_user_id=line_user_id)
        raise BadRequest("user_id or line_user_id must be provided")

    def get_all(
        self, 
        page: int = 1, 
        per_page: int = 10, 
        query: str = None, 
        status: int = None, 
        with_total_items: bool = False
    ) -> List[dict] | Tuple[List[dict], int]:
        list_dict_users = self.user_repository.select_all_by_filter(
            page, per_page, query, status
        )
        if with_total_items:
            total_items_count = self.user_repository.count_all_by_filter(query, status)
            return list_dict_users, total_items_count
        return list_dict_users

    def auth(self, credentialsObject) -> dict:
        try:
            username = credentialsObject.get("username")
            password = credentialsObject.get("password")
            user_data = self.user_repository.select_one_by_username(username=username)
        except NotFound:
            raise Unauthorized("The username or Password is incorrect.")
        
        if not check_password_hash(user_data.get("password"), password):
            raise Unauthorized("The username or Password is incorrect.")
        
        if not user_data.get("is_active"):
            raise Forbidden("User is not active")
        
        payload = {
            "sub": str(user_data.get("id")),
            "name": user_data.get("name"),
            "username": user_data.get("username"),
            "email": user_data.get("email"),
            "role": user_data.get("role")
        }
        
        return {
            "name": user_data.get("name"),
            "username": user_data.get("username"),
            "email": user_data.get("email"),
            "role": user_data.get("role"),
            "token": {
                "access_token": self.jwt_service.generate(payload),
                "token_type": "bearer",
            }
        }
