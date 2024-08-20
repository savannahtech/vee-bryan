import os
from datetime import datetime
from typing import Optional, Type

import numpy as np

from core.models.alert import Alert
from infrastructure.repositories.alert_repository import AlertRepository


class AlertService:
    def __init__(self, repository: AlertRepository):
        self.repository = repository
        self.threshold = float(
            os.getenv("ALERT_THRESHOLD", "100")
        )  # default to 100 if not set

    def check_and_create_alert(
        self, interaction_id: int, element: str, metric_value: float, metrics: list
    ):
        mean = np.mean(metrics)
        std = np.std(metrics)

        alerts = []

        # Check if metric is higher than threshold
        if metric_value > self.threshold:
            alert = Alert(
                id=0,
                interaction_id=interaction_id,
                element=element,
                metric_value=metric_value,
                alert_type="threshold",
                created_at=datetime.utcnow(),
            )
            alerts.append(self.repository.create_alert(alert))

        # Check if metric is an outlier
        if metric_value > mean + 2 * std:
            alert = Alert(
                id=0,
                interaction_id=interaction_id,
                element=element,
                metric_value=metric_value,
                alert_type="outlier",
                created_at=datetime.utcnow(),
            )
            alerts.append(self.repository.create_alert(alert))

        return alerts

    def get_alerts(self, interaction_id: Optional[int] = None) -> list[Type[Alert]]:
        return self.repository.get_alerts(interaction_id)
