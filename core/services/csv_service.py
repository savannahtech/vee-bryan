import csv
import os

from fastapi import BackgroundTasks
from sqlalchemy.orm import Session

from core.services.alert_service import AlertService
from core.services.interaction_service import InteractionService
from core.services.metric_service import MetricService
from infrastructure.repositories.alert_repository import AlertRepository
from infrastructure.repositories.interaction_repository import InteractionRepository
from infrastructure.repositories.metric_repository import MetricRepository


class CSVService:
    def __init__(self, db: Session):
        self.db = db
        self.interaction_service = InteractionService(InteractionRepository(db))
        self.metric_service = MetricService(MetricRepository(db))
        self.alert_service = AlertService(AlertRepository(db))

    def process_csv(self, file_path: str):
        with open(file_path, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                input_text = row["Input"]
                output_text = row["Output"]
                interaction = self.interaction_service.create_interaction(
                    input_text, output_text
                )
                metric = self.metric_service.calculate_and_store_metric(
                    interaction.id, input_text, output_text
                )
                all_metrics = [metric.input_metric, metric.output_metric]
                self.alert_service.check_and_create_alert(
                    interaction.id, "input", metric.input_metric, all_metrics
                )
                self.alert_service.check_and_create_alert(
                    interaction.id, "output", metric.output_metric, all_metrics
                )

    def upload_and_process_csv(self, file: bytes, background_tasks: BackgroundTasks):
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, "uploaded_file.csv")

        with open(file_path, "wb") as f:
            f.write(file)
        background_tasks.add_task(self.process_csv, file_path)
