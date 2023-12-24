from sqlalchemy import select, or_
from web_api.db.connect import get_session
from web_api.db.models import Service
from werkzeug.exceptions import NotFound, Conflict

class ServiceRepository:
    def create_one(self, new_service_data: dict):
        new_service = Service(**new_service_data)
        with get_session() as session:
            session.add(new_service)
            session.commit()
            session.refresh(new_service)
            return new_service.to_dict()


    def update_one_by_id(self, service_id: str, service_data: dict):
        with get_session() as session:
            service = session.query(Service).filter(Service.id == service_id).first()
            if service is None:
                raise NotFound("Service not found")
            
            for field, value in service_data.items():
                if value is not None:
                    setattr(service, field, value)

            session.commit()
            session.refresh(service)
            return service.to_dict()


    def logical_delete_one_by_id(self, service_id: str):
        with get_session() as session:
            service = session.query(Service).filter(Service.id == service_id).first()
            if service is None:
                raise NotFound("Service not found")
            if service.is_deleted:
                raise Conflict(f"Service `{service.name}` already deleted")
            service.is_deleted = True
            session.commit()
            session.refresh(service)
            return service.to_dict()


    def get_one_by_unique_filed(self, service_id: str):
        with get_session() as session:
            service = session.query(Service).filter(Service.id == service_id).first()
            if service is None:
                raise NotFound("Service not found")
            return service.to_dict()


    def count_all_by_filter(
        self, 
        query: str = None,
        status: int = None
    ):
        with get_session() as session:
            base_query = select(Service).filter(Service.is_deleted == False).order_by(Service.created_at.desc())
            if status == 0:
                base_query = base_query.filter(Service.is_active == False)

            if status == 1:
                base_query = base_query.filter(Service.is_active == True)

            if query is not None:
                search_filter = or_(
                    Service.name.ilike(f'%{query}%'),
                    Service.description.ilike(f'%{query}%')
                )
                base_query = base_query.filter(search_filter)

            return len(session.scalars(base_query).all())


    def get_all_by_filter(
        self,
        page: int,
        per_page: int,
        query: str,
        status: int,
    ):
        with get_session() as session:
            base_query = select(Service).filter(Service.is_deleted == False).order_by(Service.created_at.desc())
            if status == 0:
                base_query = base_query.filter(Service.is_active == False)

            if status == 1:
                base_query = base_query.filter(Service.is_active == True)

            if query is not None:
                search_filter = or_(
                    Service.name.ilike(f'%{query}%'),
                    Service.description.ilike(f'%{query}%')
                )
                base_query = base_query.filter(search_filter)

            return session.scalars(base_query).offset((page - 1) * per_page).limit(per_page).all()