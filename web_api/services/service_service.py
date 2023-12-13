from flask import abort
from sqlalchemy.exc import SQLAlchemyError
from web_api.db.connect import Session
from web_api.db.models import Service


def create_one(service_data: dict) -> Service:
    try:
        service = Service(
            name=service_data.get("name"),
            price=service_data.get("price"),
            image=service_data.get("image"),
            period_time=service_data.get("period_time"),
            open_time=service_data.get("open_time"),
            close_time=service_data.get("close_time"),
            start_date=service_data.get("start_date"),
            end_date=service_data.get("end_date"),
            unavailable_datetime=service_data.get("unavailable_datetime"),
            is_active=service_data.get("is_active"),
        )
        with Session() as session:
            session.add(service)
            session.commit()
            session.refresh(service)
            return service
    except SQLAlchemyError as e:
        abort(500, e)
    except Exception as e:
        abort(500, e)


def logical_delete(service_id: str) -> Service:
    try:
        with Session() as session:
            service = session.query(Service).filter(Service.id == service_id).first()
            if not service:
                abort(404, "Service not found")
            service.is_deleted = True
            session.commit()
            return service
    except SQLAlchemyError as e:
        abort(500, e)
    except Exception as e:
        abort(500, e)


def update_one(service_id: str, service_data: dict) -> Service:
    try:
        with Session() as session:
            service = session.query(Service).filter(Service.id == service_id).first()
            if not service:
                abort(404, "Service not found")
            for field, value in service_data.items():
                if hasattr(service, field):
                    if getattr(service, field) != value:
                        setattr(service, field, value)
            session.commit()
            session.refresh(service)
            return service
    except SQLAlchemyError as e:
        abort(500, e)
    except Exception as e:
        abort(500, e)



def get_one(service_id: str) -> Service:
    try:
        with Session() as session:
            service = session.query(Service).filter(Service.id == service_id).first()
            if not service:
                abort(404, "Service not found")
            return service
    except SQLAlchemyError as e:
        abort(500, e)
    except Exception as e:
        abort(500, e)



def get_all_available_by_pagination(page: int, per_page: int, with_total_items: bool = False) -> list:
    try:
        with Session() as session:
            if with_total_items:
                total_available_services = session.query(Service).filter(Service.is_deleted == False).count()
            services = session.query(Service).filter(Service.is_deleted == False).offset((page - 1) * per_page).limit(per_page).all()
            if with_total_items:
                return services, total_available_services
            return services
    except SQLAlchemyError as e:
        abort(500, e)
    except Exception as e:
        abort(500, e)