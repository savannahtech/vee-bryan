from sqlalchemy.orm import Session

from core.models.metric import Metric
from infrastructure.database import MetricModel


class MetricRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_metric(self, metric: Metric):
        db_metric = MetricModel(
            interaction_id=metric.interaction_id,
            input_metric=metric.input_metric,
            output_metric=metric.output_metric,
        )
        self.db.add(db_metric)
        self.db.commit()
        self.db.refresh(db_metric)
        return db_metric
