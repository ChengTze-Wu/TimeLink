from sqlalchemy import select, or_
from app.db.connect import get_session
from app.db.models import Service, WorkingHour, UnavailablePeriod, Group
from werkzeug.exceptions import NotFound, Conflict
from typing import List

class ServiceRepository:
    def insert_one(self, new_service_data: dict, working_hours: List[dict]=None, unavailable_periods: List[dict]=None, group_ids: list=None):
        with get_session() as session:
            new_service = Service(
                **new_service_data, 
                working_hours=[WorkingHour(**working_hour) for working_hour in working_hours],
                unavailable_periods=[UnavailablePeriod(**unavailable_period) for unavailable_period in unavailable_periods]
            )

            session.add(new_service)

            if group_ids is not None:
                for group_id in group_ids:
                    group = session.query(Group).filter(Group.id == group_id).first()
                    if group is None:
                        raise NotFound(f"Group not found when creating service.")
                    new_service.groups.append(group)

            session.commit()
            session.refresh(new_service)
            return new_service.to_dict()


    def update_one_by_id(self, service_id: str, service_data: dict, group_ids: list=None, working_hours: list[dict]=None) -> dict:
        with get_session() as session:
            service = session.query(Service).filter(Service.id == service_id).first()
            if service is None:
                raise NotFound("Service not found")

            if group_ids is not None:
                service.groups.clear()
                for group_id in group_ids:
                    group = session.query(Group).filter(Group.id == group_id).first()
                    if group is None:
                        raise NotFound(f"Group not found when updating service `{service.name}`.")
                    service.groups.append(group)
            
            if working_hours is not None:
                session.query(WorkingHour).filter(WorkingHour.service_id == service_id).delete()
                new_hours = [WorkingHour(service_id=service_id, **wh_data) for wh_data in working_hours]
                session.bulk_save_objects(new_hours)
            
            for field, value in service_data.items():
                if value is not None:
                    setattr(service, field, value)

            session.commit()
            session.refresh(service)
            return service.to_dict()


    def logical_delete_one_by_id(self, service_id: str) -> dict:
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


    def select_one_by_unique_filed(self, service_id: str) -> dict:
        with get_session() as session:
            service = session.query(Service).filter(Service.id == service_id).first()
            if service is None:
                raise NotFound("Service not found")
            return service.to_dict()


    def count_all_by_filter(
        self, 
        query: str = None,
        status: int = None,
        owner_id: str = None
    ) -> int:
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

            if owner_id is not None:
                base_query = base_query.filter(Service.owner_id == owner_id)

            return len(session.scalars(base_query).all())


    def select_all_by_filter(
        self,
        page: int,
        per_page: int,
        query: str,
        status: int,
        owner_id: str = None
    ) -> List[dict]:
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
            base_query = base_query.offset((page - 1) * per_page).limit(per_page)

            if owner_id is not None:
                base_query = base_query.filter(Service.owner_id == owner_id)

            services = session.scalars(
                base_query
            ).all()
            return [service.to_dict() for service in services] if services else []