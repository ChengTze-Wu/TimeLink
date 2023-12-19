from flask import abort, current_app
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import select, or_
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import NotFound, Conflict, Unauthorized, Forbidden
from web_api.db.connect import Session
from web_api.db.models import User
from typing import List, Tuple
import jwt
import datetime


def create_one(user_data: dict) -> dict:
    try:
        user = User(
            id=user_data.get("id"),
            email=user_data.get("email"),
            username=user_data.get("username"),
            password=generate_password_hash(user_data.get("password")),
            name=user_data.get("name"),
            phone=user_data.get("phone"),
            is_active=user_data.get("is_active"),
            is_deleted=user_data.get("is_deleted"),
        )
        with Session() as session:
            session.add(user)
            session.commit()
            session.refresh(user)
            return user.to_dict()
    except SQLAlchemyError as e:
        if isinstance(e, IntegrityError):
            if "Key (email)" in str(e.orig):
                abort(409, f"Email `{user_data['email']}` already exists")
            if "Key (username)" in str(e.orig):
                abort(409, f"Username `{user_data['username']}` already exists")
        abort(500, e)
    except Exception as e:
        abort(500, e)


def update_one_by_id(user_data: dict, user_id: str) -> dict:
    try:
        with Session() as session:
            user = session.scalars(
                select(User).filter(User.id == user_id)
            ).first()
            if user is None:
                raise NotFound(f"User not found")

            for field, value in user_data.items():
                if hasattr(user, field):
                    if getattr(user, field) != value:
                        if field == "password":
                            value = generate_password_hash(value)
                        setattr(user, field, value)

            session.commit()
            session.refresh(user)
            return user.to_dict()
    except NotFound as e:
        abort(404, e.description)
    except SQLAlchemyError as e:
        if isinstance(e, IntegrityError):
            if "Key (email)" in str(e.orig):
                abort(409, f"Email `{user_data['email']}` already exists")
            if "Key (username)" in str(e.orig):
                abort(409, f"Username `{user_data['username']}` already exists")
    except Exception as e:
        abort(500, e)


def logical_delete_by_id(user_id: str) -> dict:
    try:
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
    except Conflict as e:
        abort(409, e.description)
    except NotFound as e:
        abort(404, e.description)
    except Exception as e:
        abort(500, e)


def get_one_by_id(user_id: str) -> dict:
    try:
        with Session() as session:
            user = session.scalars(
                select(User).filter(User.id == user_id)
            ).first()
            if user is None:
                raise NotFound(f"User not found")
            return user.to_dict()
    except NotFound as e:
        abort(404, e.description)
    except Exception as e:
        abort(500, e)


def get_all_available_by_filter(
    page: int = 1, per_page: int = 10, query: str = None, status: int = None, with_total_items: bool = True
) -> List[dict] | Tuple[List[dict], int]:
    try:
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

            users = session.scalars(
                base_query.offset((page - 1) * per_page).limit(per_page)
            ).all()
            list_dict_users = [user.to_dict() for user in users]

            if with_total_items is True:
                total_items = len(session.scalars(base_query).all())
                return list_dict_users, total_items

            return list_dict_users
    except Exception as e:
        abort(500, e)


def login(username: str, password: str) -> str:
    """
    Return JWT token
    """
    try:
        with Session() as session:
            user = session.scalars(
                select(User).filter(
                    User.username == username and User.is_deleted == False
                )
            ).first()
            if user is None or not check_password_hash(user.password, password):
                raise Unauthorized(f"Invalid username or password")
            if not user.is_active:
                raise Forbidden(f"User `{username}` is not active")

            JWT_SECRET_KEY = current_app.config.get("JWT_SECRET_KEY", "test")
            JWT_ACCESS_TOKEN_EXPIRE_HOURS = current_app.config.get(
                "JWT_ACCESS_TOKEN_EXPIRE_HOURS", 24
            )
            jwt_payload = {
                "username": user.username,
                "name": user.name,
                "email": user.email,
                "exp": datetime.datetime.now(tz=datetime.timezone.utc)
                + datetime.timedelta(hours=JWT_ACCESS_TOKEN_EXPIRE_HOURS),
            }

            jwt_token = jwt.encode(payload=jwt_payload, key=JWT_SECRET_KEY, algorithm="HS256")

        return jwt_token
    except NotFound as e:
        abort(404, e.description)
    except Unauthorized as e:
        abort(401, e.description)
    except Forbidden as e:
        abort(403, e.description)
    except Exception as e:
        abort(500, e)
