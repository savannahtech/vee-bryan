from core.models.metric import Metric
from infrastructure.repositories.metric_repository import MetricRepository


class MetricService:
    def __init__(self, repository: MetricRepository):
        self.repository = repository

    def calculate_and_store_metric(
        self, interaction_id: int, input_text: str, output_text: str
    ) -> Metric:
        input_metric = len(input_text)  # Example metric: length of the input text
        output_metric = len(output_text)  # Example metric: length of the output text
        metric = Metric(
            id=0,
            interaction_id=interaction_id,
            input_metric=input_metric,
            output_metric=output_metric,
        )
        return self.repository.create_metric(metric)
