from sqlalchemy import select, or_, func
from app.db.connect import get_session
from app.db.models import Group, User, Service
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from werkzeug.exceptions import NotFound, Conflict, Forbidden


class GroupRepository:
    def insert_one(self, new_group_data: dict):
        try:
            new_group = Group(**new_group_data)
            with get_session() as session:
                session.add(new_group)
                session.commit()
                session.refresh(new_group)
                return new_group.to_self_dict()
        except SQLAlchemyError as e:
            if isinstance(e, IntegrityError):
                if "Key (line_group_id)" in str(e.orig):
                    raise Conflict(
                        f"Line group id `{new_group.line_group_id}` already exists"
                    )
            raise e

    def update_one_by_id(
        self,
        group_id: str,
        group_data: dict,
    ):
        with get_session() as session:
            group = (
                session.query(Group)
                .filter(Group.id == group_id, Group.is_deleted == False)
                .first()
            )
            if group is None:
                raise NotFound("Group not found")

            for field, value in group_data.items():
                if value is not None:
                    setattr(group, field, value)

            session.commit()
            session.refresh(group)
            return group.with_owner_dict()

    def logical_delete_one_by_id(self, group_id: str):
        with get_session() as session:
            group = session.query(Group).filter(Group.id == group_id).first()
            if group is None:
                raise NotFound(f"Group not found")
            if group.is_deleted:
                raise Conflict(f"Group `{group.name}` already deleted")
            group.is_deleted = True
            session.commit()
            session.refresh(group)
            return group.with_owner_dict()

    def select_one_by_unique_filed(
        self, group_id: str = None, line_group_id: str = None, owner_id: str = None
    ):
        with get_session() as session:
            base_query = select(Group).filter(Group.is_deleted == False)
            if group_id is not None:
                base_query = base_query.filter(Group.id == group_id)
            if line_group_id is not None:
                base_query = base_query.filter(Group.line_group_id == line_group_id)
            if owner_id is not None:
                base_query = base_query.filter(Group.owner_id == owner_id)

            group = session.execute(base_query).scalar_one_or_none()
            if group is None:
                raise NotFound("Group not found")
            return group.with_owner_dict()

    def count_all_by_filter(
        self,
        query: str = None,
        status: int = None,
        owner_id: str = None,
    ):
        with get_session() as session:
            base_query = (
                select(func.count(Group.id))
                .filter(Group.is_deleted == False)
            )
            if status == 0:
                base_query = base_query.filter(Group.is_active == False)

            if status == 1:
                base_query = base_query.filter(Group.is_active == True)

            if query is not None:
                search_filter = or_(Group.name.ilike(f"%{query}%"))
                base_query = base_query.filter(search_filter)

            if owner_id is not None:
                base_query = base_query.filter(Group.owner_id == owner_id)

            count_result = session.execute(base_query).scalar_one()
            return count_result

    def select_all_by_filter(
        self,
        page: int = 1,
        per_page: int = 10,
        query: str = None,
        status: int = None,
        owner_id: str = None,
        service_id: str = None,
        with_by: str = "self",
    ):
        with get_session() as session:
            base_query = (
                select(Group)
                .filter(Group.is_deleted == False)
                .order_by(Group.created_at.desc())
            )
            if status == 0:
                base_query = base_query.filter(Group.is_active == False)

            if status == 1:
                base_query = base_query.filter(Group.is_active == True)

            if query is not None:
                search_filter = or_(Group.name.ilike(f"%{query}%"))
                base_query = base_query.filter(search_filter)

            if owner_id is not None:
                base_query = base_query.filter(Group.owner_id == owner_id)

            if service_id is not None:
                base_query = base_query.join(Service, Group.services).filter(
                    Service.id == service_id
                )

            base_query = base_query.offset((page - 1) * per_page).limit(per_page)
            groups = session.scalars(base_query)

            match with_by:
                case "self":
                    return [group.to_self_dict() for group in groups] if groups else []
                case "owner":
                    return [group.with_owner_dict() for group in groups] if groups else []
                case _:
                    raise ValueError("with_by must be one of 'self', 'services', 'owner'")

    def add_user_to_group_by_line_ids(self, line_group_id: str, line_user_id: str):
        with get_session() as session:
            group = (
                session.query(Group)
                .filter(Group.line_group_id == line_group_id, Group.is_deleted == False)
                .first()
            )
            if group is None:
                raise NotFound("Group not found with provided line_group_id")

            user = (
                session.query(User)
                .filter(User.line_user_id == line_user_id, User.is_deleted == False)
                .first()
            )
            if user is None:
                raise NotFound("User not found with provided line_user_id")

            if user in group.users:
                raise Conflict("User already in group")

            group.users.append(user)
            session.commit()
            return group.with_owner_dict()

    def remove_user_from_group_by_line_ids(self, line_group_id: str, line_user_id: str):
        with get_session() as session:
            group = (
                session.query(Group)
                .filter(Group.line_group_id == line_group_id, Group.is_deleted == False)
                .first()
            )
            if group is None:
                raise NotFound("Group not found with provided line_group_id")

            user = (
                session.query(User)
                .filter(User.line_user_id == line_user_id, User.is_deleted == False)
                .first()
            )
            if user is None:
                raise NotFound("User not found with provided line_user_id")

            if user not in group.users:
                raise NotFound("User not in the specified group")

            group.users.remove(user)
            session.commit()
            return group.with_owner_dict()

    def check_groups_owner_by_user_id(self, user_id: str, group_ids: list):
        with get_session() as session:
            groups = (
                session.query(Group)
                .filter(Group.id.in_(group_ids), Group.is_deleted == False)
                .all()
            )
            for group in groups:
                if str(group.owner_id) != user_id:
                    return False
            return True
