from sqlalchemy.orm import Session

from core.models.alert import Alert
from infrastructure.database import AlertModel


class AlertRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_alert(self, alert: Alert):
        db_alert = AlertModel(
            interaction_id=alert.interaction_id,
            element=alert.element,
            metric_value=alert.metric_value,
            alert_type=alert.alert_type,
            created_at=alert.created_at,
        )
        self.db.add(db_alert)
        self.db.commit()
        self.db.refresh(db_alert)
        return db_alert

    def get_alerts(self, interaction_id: int = None):
        query = self.db.query(AlertModel)
        if interaction_id:
            query = query.filter(AlertModel.interaction_id == interaction_id)
        return query.all()
