from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import select, or_, func
from werkzeug.exceptions import NotFound, Conflict, BadRequest
from app.db.connect import get_session
from app.db.models import User, Role


class UserRepository:
    def insert_one(self, new_user_data: dict, role: str = None):
        try:
            error_datails = []
            with get_session() as session:
                new_user = User(**new_user_data)
                if role is not None:
                    role_entity = session.query(Role).filter(Role.name == role).first()
                    if role_entity is None:
                        raise BadRequest(f"Role `{role}` not found")
                    new_user.role = role_entity
                session.add(new_user)
                session.commit()
                session.refresh(new_user)
                return new_user.to_self_dict()
        except SQLAlchemyError as e:
            if isinstance(e, IntegrityError):
                if "Key (email)" in str(e.orig):
                    error_datails.append(f"Email `{new_user.email}` already exists")
                if "Key (username)" in str(e.orig):
                    error_datails.append(
                        f"Username `{new_user.username}` already exists"
                    )
                if "Key (line_user_id)" in str(e.orig):
                    error_datails.append(
                        f"Line user id `{new_user.line_user_id}` already exists"
                    )
                raise Conflict(error_datails)
            raise e

    def update_one_by_id(self, user_id: str, user_data: dict, role: str = None):
        try:
            error_datails = []
            with get_session() as session:
                user = (
                    session.query(User)
                    .filter(User.id == user_id, User.is_deleted == False)
                    .first()
                )
                if user is None:
                    raise NotFound("User not found")

                if role is not None:
                    role_entity = session.query(Role).filter(Role.name == role).first()
                    if role_entity is None:
                        raise BadRequest(f"Role `{role}` not found")
                    user.role = role_entity

                for field, value in user_data.items():
                    if value is not None:
                        setattr(user, field, value)

                session.commit()
                session.refresh(user)
                return user.to_self_dict()
        except SQLAlchemyError as e:
            if isinstance(e, IntegrityError):
                if "Key (email)" in str(e.orig):
                    error_datails.append(f"Email `{user_data['email']}` already exists")
                if "Key (username)" in str(e.orig):
                    error_datails.append(
                        f"Username `{user_data['username']}` already exists"
                    )
                raise Conflict(error_datails)
            raise e

    def logical_delete_one_by_id(self, user_id: str):
        with get_session() as session:
            user = session.query(User).filter(User.id == user_id).first()
            if user is None:
                raise NotFound(f"User not found")
            if user.is_deleted:
                raise Conflict(f"User `{user.username}` already deleted")
            user.is_deleted = True
            session.commit()
            session.refresh(user)
            return user.to_self_dict()

    def select_one_by_unique_filed(
        self,
        user_id: str = None,
        line_user_id: str = None,
        email: str = None,
    ):
        with get_session() as session:
            base_query = select(User).filter(User.is_deleted == False)
            if user_id is not None:
                user = session.execute(base_query.filter(User.id == user_id)).scalar_one()

            if line_user_id is not None:
                user = (
                    session.execute(base_query.filter(User.line_user_id == line_user_id))
                    .scalar_one()
                )

            if email is not None:
                user = (
                    session.execute(base_query.filter(User.email == email)).scalar_one()
                )

            if user is None:
                raise NotFound("User not found")
            return user.to_self_dict()

    def select_one_by_username(self, username: str):
        with get_session() as session:
            user = (
                session.query(User)
                .filter(User.username == username, User.is_deleted == False)
                .first()
            )
            if user is None:
                raise NotFound("User not found")
            return user.to_auth()

    def count_all_by_filter(self, group_id: str = None, query: str = None, status: int = None):
        with get_session() as session:
            base_query = (
                select(func.count(User.id))
                .filter(User.is_deleted == False)
            )
            if status == 0:
                base_query = base_query.filter(User.is_active == False)

            if status == 1:
                base_query = base_query.filter(User.is_active == True)

            if query is not None:
                search_filter = or_(
                    User.email.ilike(f"%{query}%"),
                    User.username.ilike(f"%{query}%"),
                    User.name.ilike(f"%{query}%"),
                    User.phone.ilike(f"%{query}%"),
                )
                base_query = base_query.filter(search_filter)

            if group_id is not None:
                base_query = base_query.filter(User.groups.any(id=group_id))

            count_result = session.execute(base_query).scalar_one()
            return count_result

    def select_all_by_filter(
        self,
        page: int,
        per_page: int,
        query: str,
        status: int,
        group_id: str = None,
    ):
        with get_session() as session:
            base_query = (
                select(User)
                .filter(User.is_deleted == False)
                .order_by(User.created_at.desc())
            )
            if status == 0:
                base_query = base_query.filter(User.is_active == False)

            if status == 1:
                base_query = base_query.filter(User.is_active == True)

            if query is not None:
                search_filter = or_(
                    User.email.ilike(f"%{query}%"),
                    User.username.ilike(f"%{query}%"),
                    User.name.ilike(f"%{query}%"),
                    User.phone.ilike(f"%{query}%"),
                )
                base_query = base_query.filter(search_filter)

            if group_id is not None:
                base_query = base_query.filter(User.groups.any(id=group_id))
            
            base_query = base_query.offset((page - 1) * per_page).limit(per_page)
            users = session.scalars(base_query)
            return [user.to_self_dict() for user in users] if users else []
