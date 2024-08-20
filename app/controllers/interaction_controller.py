from fastapi import APIRouter, BackgroundTasks, Depends, File, UploadFile
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.utils.response_helper import create_response
from core.services.alert_service import AlertService
from core.services.csv_service import CSVService
from core.services.interaction_service import InteractionService
from core.services.metric_service import MetricService
from infrastructure.database import get_db
from infrastructure.repositories.alert_repository import AlertRepository
from infrastructure.repositories.interaction_repository import InteractionRepository
from infrastructure.repositories.metric_repository import MetricRepository

router = APIRouter()


class InteractionRequest(BaseModel):
    input_text: str
    output_text: str


@router.post("")
def create_interaction(
    interaction_request: InteractionRequest, db: Session = Depends(get_db)
):
    interaction_service = InteractionService(InteractionRepository(db))
    interaction = interaction_service.create_interaction(
        interaction_request.input_text, interaction_request.output_text
    )

    metric_service = MetricService(MetricRepository(db))
    metric = metric_service.calculate_and_store_metric(
        interaction.id, interaction_request.input_text, interaction_request.output_text
    )

    alert_service = AlertService(AlertRepository(db))
    all_metrics = [metric.input_metric, metric.output_metric]
    alerts = alert_service.check_and_create_alert(
        interaction.id, "input", metric.input_metric, all_metrics
    )
    alerts += alert_service.check_and_create_alert(
        interaction.id, "output", metric.output_metric, all_metrics
    )

    return create_response(
        success=True, data=interaction, message="Interaction created successfully"
    )


@router.get("")
def get_interactions(db: Session = Depends(get_db)):
    interaction_service = InteractionService(InteractionRepository(db))
    interactions = interaction_service.get_interactions()
    return create_response(
        success=True, data=interactions, message="Interactions fetched successfully"
    )


@router.post("/bulk")
async def upload_csv(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    csv_service = CSVService(db)
    file_bytes = await file.read()
    csv_service.upload_and_process_csv(file_bytes, background_tasks)
    return create_response(
        success=True, message="CSV file received. Processing in the background."
    )
