from dataclasses import dataclass


@dataclass
class Metric:
    id: int
    interaction_id: int
    input_metric: float
    output_metric: float
