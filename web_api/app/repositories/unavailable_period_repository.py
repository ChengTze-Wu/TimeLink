from app.db.connect import get_session
from app.db.models import UnavailablePeriod
from werkzeug.exceptions import NotFound
from typing import List


class UnavailablePeriodRepository:
    def insert_bulk(self, service_id: str, new_unavailable_periods: List[dict]):
        new_unavailable_periods = [
            UnavailablePeriod(service_id=service_id, **new_unavailable_period)
            for new_unavailable_period in new_unavailable_periods
        ]
        with get_session() as session:
            session.bulk_save_objects(new_unavailable_periods)
            session.commit()
            return True

    def update_bulk(self, update_unavailable_periods: List[dict]):
        with get_session() as session:
            for update_unavailable_period in update_unavailable_periods:
                unavailable_period = (
                    session.query(UnavailablePeriod)
                    .filter(UnavailablePeriod.id == update_unavailable_period.get("id"))
                    .first()
                )
                if unavailable_period is None:
                    raise NotFound("Unavailable Period not found")

                for field, value in update_unavailable_period.items():
                    if value is not None:
                        setattr(unavailable_period, field, value)

            session.commit()
            return True

    def delete_bulk_by_ids(self, delete_unavailable_period_ids: List[str]):
        with get_session() as session:
            for delete_unavailable_period_id in delete_unavailable_period_ids:
                unavailable_period = (
                    session.query(UnavailablePeriod)
                    .filter(UnavailablePeriod.id == delete_unavailable_period_id)
                    .first()
                )
                if unavailable_period is None:
                    raise NotFound("Working Hour not found")
                session.delete(unavailable_period)

            session.commit()
            return True
