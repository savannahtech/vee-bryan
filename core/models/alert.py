from dataclasses import dataclass
from datetime import datetime


@dataclass
class Alert:
    id: int
    interaction_id: int
    element: str
    metric_value: float
    alert_type: str
    created_at: datetime
