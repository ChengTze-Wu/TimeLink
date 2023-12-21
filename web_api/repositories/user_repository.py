from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import select, or_
from werkzeug.exceptions import NotFound, Conflict
from web_api.db.connect import Session
from web_api.db.models import User


class UserRepository:
    def create_new_user(
        self,
        new_user_data: dict
    ):
        try:
            error_datails = []
            new_user = User(**new_user_data)
            with Session() as session:
                session.add(new_user)
                session.commit()
                session.refresh(new_user)
                return new_user.to_dict()
        except SQLAlchemyError as e:
            if isinstance(e, IntegrityError):
                if "Key (email)" in str(e.orig):
                    error_datails.append(f"Email `{new_user.email}` already exists")
                if "Key (username)" in str(e.orig):
                    error_datails.append(f"Username `{new_user.username}` already exists")
                raise Conflict(error_datails)
            raise e

    def update_user_by_id(
        self,
        user_id: str,
        user_data: dict
    ):
        error_datails = []
        try:
            with Session() as session:
                user = session.query(User).filter(User.id == user_id).first()
                if user is None:
                    raise NotFound("User not found")

                for field, value in user_data.items():
                    if value is not None:
                        setattr(user, field, value)


                session.commit()
                session.refresh(user)
                return user.to_dict()
        except SQLAlchemyError as e:
            if isinstance(e, IntegrityError):
                if "email" in str(e.orig):
                    error_datails.append(f"Email `{user_data['email']}` already exists")
                if "username" in str(e.orig):
                    error_datails.append(f"Username `{user_data['username']}` already exists")
                raise Conflict(error_datails)
            raise e

    def logical_delete_user_by_id(
        self,
        user_id: str
    ):
        with Session() as session:
            user = session.query(User).filter(User.id == user_id).first()
            if user is None:
                raise NotFound(f"User not found")
            if user.is_deleted:
                raise Conflict(f"User `{user.username}` already deleted")
            user.is_deleted = True
            session.commit()
            session.refresh(user)
            return user.to_dict()
        
    def get_one_by_id(
        self,
        user_id: str
    ):
        with Session() as session:
            user = session.query(User).filter(User.id == user_id).first()
            if user is None:
                raise NotFound("User not found")
            return user.to_dict()
        

    def count_all_users_by_filter(
        self,
        query: str = None,
        status: int = None
    ):
        with Session() as session:
            base_query = select(User).filter(User.is_deleted == False).order_by(User.created_at.desc())
            if status == 0:
                base_query = base_query.filter(User.is_active == False)

            if status == 1:
                base_query = base_query.filter(User.is_active == True)

            if query is not None:
                search_filter = or_(
                    User.email.ilike(f'%{query}%'),
                    User.username.ilike(f'%{query}%'),
                    User.name.ilike(f'%{query}%'),
                    User.phone.ilike(f'%{query}%')
                )
                base_query = base_query.filter(search_filter)

            return len(session.scalars(base_query).all())
        

    def get_users_by_filter(
        self,
        page: int = 1,
        per_page: int = 10,
        query: str = None,
        status: int = None
    ):
        with Session() as session:
            base_query = select(User).filter(User.is_deleted == False).order_by(User.created_at.desc())
            if status == 0:
                base_query = base_query.filter(User.is_active == False)

            if status == 1:
                base_query = base_query.filter(User.is_active == True)

            if query is not None:
                search_filter = or_(
                    User.email.ilike(f'%{query}%'),
                    User.username.ilike(f'%{query}%'),
                    User.name.ilike(f'%{query}%'),
                    User.phone.ilike(f'%{query}%')
                )
                base_query = base_query.filter(search_filter)
            base_query = base_query.offset((page - 1) * per_page).limit(per_page)
            users = session.scalars(
                base_query
            )
            return [user.to_dict() for user in users]