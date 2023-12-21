from typing import List, Tuple
from werkzeug.exceptions import NotFound, Conflict
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from web_api.db.connect import Session
from web_api.db.models import Group
from sqlalchemy import select


def create_one(group_data: dict) -> dict:
    try:
        group = Group(
            id=group_data['id'],
            name=group_data['name'],
            line_group_id=group_data['line_group_id'],
            is_active=group_data['is_active'],
        )
        with Session() as session:
            session.add(group)
            session.commit()
            session.refresh(group)
            return group.to_dict()
    except SQLAlchemyError as e:
        if isinstance(e, IntegrityError):
            if "Key (line_group_id)" in str(e.orig):
                raise Conflict(f"Group line_group_id `{group_data['line_group_id']}` already exists")


def update_one_by_id(group_data: dict, group_id: str) -> dict:
    with Session() as session:
        group = session.query(Group).filter(Group.id == group_id).first()
        if not group:
            raise NotFound("Group not found")
        for field, value in group_data.items():
            if hasattr(group, field):
                if getattr(group, field) != value:
                    setattr(group, field, value)
        session.commit()
        session.refresh(group)
        return group.to_dict()


def logical_delete_by_id(group_id: str) -> dict:
    with Session() as session:
        group = session.query(Group).filter(Group.id == group_id).first()
        if group is None:
            raise NotFound("Group not found")
        if group.is_deleted:
            raise Conflict(f"Group `{group.name}` already deleted")
        group.is_deleted = True
        session.commit()
        session.refresh(group)
        return group.to_dict()


def get_one_by_id(group_id: str) -> dict:
    with Session() as session:
        group = session.query(Group).filter(Group.id == group_id).first()
        if group is None:
            raise NotFound("Group not found")
        return group.to_dict()


def get_all_available_by_filter(
    page: int = 1, per_page: int = 10, query: str = None, status: int = None, with_total_items: bool = True
) -> List[dict] | Tuple[List[dict], int]:
    with Session() as session:
        base_query = select(Group).filter(Group.is_deleted == False).order_by(Group.created_at.desc())

        if status == 0:
            base_query = base_query.filter(Group.is_active == False)

        if status == 1:
            base_query = base_query.filter(Group.is_active == True)

        if query is not None:
            base_query = base_query.filter(Group.name.ilike(f"%{query}%"))

        groups = session.scalars(base_query.offset((page - 1) * per_page).limit(per_page)).all()
        list_dict_groups = [group.to_dict() for group in groups]

        if with_total_items:
            total_items = len(session.scalars(base_query).all())
            return list_dict_groups, total_items
        return list_dict_groups