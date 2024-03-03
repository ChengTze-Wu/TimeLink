from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import NotFound, Forbidden, Unauthorized
from app.repositories import UserRepository, GroupRepository
from typing import List, Tuple
from app.db.models import RoleName
from werkzeug.exceptions import BadRequest
from app.utils.handlers.jwt_handler import JWTHandler


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()
        self.group_repository = GroupRepository()

    def create_one(self, user_json_data: dict, payload: dict | None = {}) -> dict:
        client_role = payload.get("role")
        create_role = user_json_data.get("role")

        if client_role != RoleName.ADMIN.value and create_role == RoleName.ADMIN.value:
            raise Forbidden("Only admin can select admin")

        if create_role is not None and create_role.lower() not in [
            create_role.value for create_role in RoleName
        ]:
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
        return self.user_repository.insert_one(
            new_user_data, create_role.upper() if create_role is not None else None
        )

    def update_one(self, user_id: str, user_json_data: dict, payload: dict | None = {}) -> dict:
        create_role = user_json_data.get("role")
        client_role = payload.get("role")

        if client_role != RoleName.ADMIN.value and create_role == RoleName.ADMIN.value:
            raise Forbidden("Only admin can select admin")

        if create_role is not None and create_role.lower() not in [
            create_role.value for create_role in RoleName
        ]:
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
        return self.user_repository.update_one_by_id(
            user_id,
            update_user_data,
            create_role.upper() if create_role is not None else None,
        )

    def delete_one(self, user_id: str) -> dict:
        return self.user_repository.logical_delete_one_by_id(user_id)

    def get_one(self, user_id: str = None, line_user_id: str = None):
        if user_id:
            user_data = self.user_repository.select_one_by_unique_filed(user_id=user_id)
        elif line_user_id:
            user_data = self.user_repository.select_one_by_unique_filed(line_user_id=line_user_id)
        else:
            raise BadRequest("User id or line user id is required")

        return user_data

    def get_all(
        self,
        page: int = 1,
        per_page: int = 10,
        query: str = None,
        status: int = None,
        group_id: str = None,
        with_total_items: bool = False,
        payload: dict | None = {},
    ) -> List[dict] | Tuple[List[dict], int]:
        if payload.get("role") == RoleName.GROUP_OWNER.value:
            is_user_own_groups = self.group_repository.check_groups_owner_by_user_id(
                user_id=payload.get("sub"), group_ids=[group_id]
            )
            if not is_user_own_groups:
                raise Forbidden("You are not owner of this group")

        list_dict_users = self.user_repository.select_all_by_filter(
            page, per_page, query, status, group_id
        )
        if with_total_items:
            total_items_count = self.user_repository.count_all_by_filter(group_id, query, status)
            return list_dict_users, total_items_count
        return list_dict_users

    def auth(self, credentialsObject) -> dict:
        try:
            jwt = JWTHandler()
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
            "role": user_data.get("role"),
        }

        return {
            "id": user_data.get("id"),
            "name": user_data.get("name"),
            "username": user_data.get("username"),
            "email": user_data.get("email"),
            "role": user_data.get("role"),
            "token": {
                "access_token": jwt.generate(payload),
                "token_type": "bearer",
                "expires_in": jwt.exp_second,
            },
        }
