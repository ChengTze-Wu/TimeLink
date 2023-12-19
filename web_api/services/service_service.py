from typing import List, Tuple
from flask import abort
from sqlalchemy import or_
from web_api.db.connect import Session
from web_api.db.models import Service, UnavailablePeriod
from werkzeug.exceptions import NotFound, Conflict

def create_one(service_data: dict) -> dict:
    try:
        unavailable_periods_dataset = service_data.get("unavailable_periods", [])

        unavailable_periods = [
            UnavailablePeriod(
                start_datetime=service_data.get("start_datetime"),
                end_datetime=service_data.get("end_datetime"),
            )
            for unavailable_period_data in unavailable_periods_dataset if unavailable_period_data
        ]

        service = Service(
            name=service_data.get("name"),
            price=service_data.get("price"),
            image=service_data.get("image"),
            period_time=service_data.get("period_time"),
            open_time=service_data.get("open_time"),
            close_time=service_data.get("close_time"),
            start_date=service_data.get("start_date"),
            end_date=service_data.get("end_date"),
            is_active=service_data.get("is_active"),
            unavailable_periods=unavailable_periods
        )

        with Session() as session:
            session.add(service)
            session.commit()
            session.refresh(service)
            return service.to_dict()
        
    except Exception as e:
        abort(500, e)



def logical_delete_by_id(service_id: str) -> dict:
    try:
        with Session() as session:
            service = session.query(Service).filter(Service.id == service_id).first()
            if service is None:
                raise NotFound(f"Service not found")
            if service.is_deleted:
                raise Conflict(f"Service `{service.name}` already deleted")
            service.is_deleted = True
            session.commit()
            return service.to_dict()
    except NotFound as e:
        abort(404, e.description)
    except Conflict as e:
        abort(409, e.description)
    except Exception as e:
        abort(500, e)


def update_one_by_id(service_id: str, service_data: dict) -> dict:
    try:
        with Session() as session:
            service = session.query(Service).filter(Service.id == service_id).first()
            if service is None:
                raise NotFound(f"Service not found")
            for field, value in service_data.items():
                if hasattr(service, field):
                    if getattr(service, field) != value:
                        setattr(service, field, value)
            session.commit()
            session.refresh(service)
            return service.to_dict()
    except NotFound as e:
        abort(404, e.description)
    except Exception as e:
        abort(500, e)


def get_one_by_id(service_id: str) -> dict:
    try:
        with Session() as session:
            service = session.query(Service).filter(Service.id == service_id).first()
            if service is None:
                raise NotFound(f"Service not found")
            return service.to_dict()
    except NotFound as e:
        abort(404, e.description)
    except Exception as e:
        abort(500, e)



def get_all_available_by_filter(page: int = 1, per_page: int = 10, query: str = None, status: int = None, with_total_items: bool = True) -> List[dict] | Tuple[List[dict], int]:
    try:
        with Session() as session:
            base_query = session.query(Service).filter(Service.is_deleted == False).order_by(Service.created_at.desc())

            if status == 0:
                base_query = base_query.filter(Service.is_active == False)

            if status == 1:
                base_query = base_query.filter(Service.is_active == True)

            if query is not None:
                search_filter = or_(
                    Service.name.ilike(f'%{query}%'),
                    Service.price.ilike(f'%{query}%'),
                )
                base_query = base_query.filter(search_filter)

            services = session.scalars(base_query.offset((page - 1) * per_page).limit(per_page)).all()
            list_dict_services = [service.to_dict() for service in services]

            if with_total_items is True:
                total_items = len(session.scalars(base_query).all())
                return list_dict_services, total_items

            return list_dict_services

    except Exception as e:
        abort(500, e)