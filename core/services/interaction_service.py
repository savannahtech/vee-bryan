from datetime import datetime

from core.models.interaction import Interaction
from infrastructure.repositories.interaction_repository import InteractionRepository


class InteractionService:
    def __init__(self, repository: InteractionRepository):
        self.repository = repository

    def create_interaction(self, input_text: str, output_text: str) -> Interaction:
        interaction = Interaction(
            id=0, input=input_text, output=output_text, created_at=datetime.utcnow()
        )
        return self.repository.create_interaction(interaction)

    def get_interactions(self):
        return self.repository.get_interactions()
