from app.db.connect import get_session
from app.db.models import WorkingHour
from werkzeug.exceptions import NotFound
from typing import List


class WorkingHourRepository:        
    def insert_bulk(self, service_id: str, new_working_hours: List[dict]):
        new_working_hours = [WorkingHour(service_id=service_id, **new_working_hour) for new_working_hour in new_working_hours]
        with get_session() as session:
            session.bulk_save_objects(new_working_hours)
            session.commit()
            return True
        
    def update_bulk(self, update_working_hours: List[dict]):
        with get_session() as session:
            for update_working_hour in update_working_hours:
                working_hour = session.query(WorkingHour).filter(WorkingHour.id == update_working_hour.get("id")).first()
                if working_hour is None:
                    raise NotFound("Working Hour not found")
                
                for field, value in update_working_hour.items():
                    if value is not None:
                        setattr(working_hour, field, value)

            session.commit()
            return True
        
    def delete_bulk_by_ids(self, delete_working_hour_ids: List[str]):
        with get_session() as session:
            for delete_working_hour_id in delete_working_hour_ids:
                working_hour = session.query(WorkingHour).filter(WorkingHour.id == delete_working_hour_id).first()
                if working_hour is None:
                    raise NotFound("Working Hour not found")
                session.delete(working_hour)

            session.commit()
            return True