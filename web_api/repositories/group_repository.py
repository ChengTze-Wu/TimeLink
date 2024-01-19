from sqlalchemy import select, or_
from web_api.db.connect import get_session
from web_api.db.models import Group
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from werkzeug.exceptions import NotFound, Conflict

class GroupRepository:
    def create_one(
        self,
        new_group_data: dict
    ):
        try:
            error_datails = []
            new_group = Group(**new_group_data)
            with get_session() as session:
                session.add(new_group)
                session.commit()
                session.refresh(new_group)
                return new_group.to_dict()
        except SQLAlchemyError as e:
            if isinstance(e, IntegrityError):
                if "Key (id)" in str(e.orig):
                    error_datails.append(f"Id `{new_group.id}` already exists")
                if "Key (line_group_id)" in str(e.orig):
                    error_datails.append(f"Line group id `{new_group.line_group_id}` already exists")
                raise Conflict(error_datails)
            raise e

    def update_one_by_id(
        self,
        group_id: str,
        group_data: dict
    ):
        try:
            error_datails = []
            with get_session() as session:
                group = session.query(Group).filter(Group.id == group_id).first()
                if group is None:
                    raise NotFound("Group not found")

                for field, value in group_data.items():
                    if value is not None:
                        setattr(group, field, value)

                session.commit()
                session.refresh(group)
                return group.to_dict()
        except SQLAlchemyError as e:
            if isinstance(e, IntegrityError):
                if "Key (id)" in str(e.orig):
                    error_datails.append(f"Id `{group_data['id']}` already exists")
                if "Key (line_group_id)" in str(e.orig):
                    error_datails.append(f"Line group id `{group_data['line_group_id']}` already exists")
                raise Conflict(error_datails)
            raise e

    def logical_delete_one_by_id(
        self,
        group_id: str
    ):
        with get_session() as session:
            group = session.query(Group).filter(Group.id == group_id).first()
            if group is None:
                raise NotFound(f"Group not found")
            if group.is_deleted:
                raise Conflict(f"Group `{group.name}` already deleted")
            group.is_deleted = True
            session.commit()
            session.refresh(group)
            return group.to_dict()
        
    def get_one_by_unique_filed(self, group_id: str = None, line_group_id: str = None):
        with get_session() as session:
            search_filter = or_(
                Group.id == group_id,
                Group.line_group_id == line_group_id
            )
            group = session.query(Group).filter(search_filter).first()
            if group is None:
                raise NotFound(f"Group not found")
            return group.to_dict()

    def count_all_by_filter(
        self,
        query: str = None,
        status: int = None
    ):
        with get_session() as session:
            base_query = select(Group).filter(Group.is_deleted == False).order_by(Group.created_at.desc())
            if status == 0:
                base_query = base_query.filter(Group.is_active == False)

            if status == 1:
                base_query = base_query.filter(Group.is_active == True)

            if query is not None:
                search_filter = or_(
                    Group.name.ilike(f'%{query}%')
                )
                base_query = base_query.filter(search_filter)

            return len(session.scalars(base_query).all())

    def get_all_by_filter(
        self,
        page: int = 1,
        per_page: int = 10,
        query: str = None,
        status: int = None
    ):
        with get_session() as session:
            base_query = select(Group).filter(Group.is_deleted == False).order_by(Group.created_at.desc())
            if status == 0:
                base_query = base_query.filter(Group.is_active == False)

            if status == 1:
                base_query = base_query.filter(Group.is_active == True)

            if query is not None:
                search_filter = or_(
                    Group.name.ilike(f'%{query}%')
                )
                base_query = base_query.filter(search_filter)
            base_query = base_query.offset((page - 1) * per_page).limit(per_page)
            groups = session.scalars(
                base_query
            )
            return [group.to_dict() for group in groups]