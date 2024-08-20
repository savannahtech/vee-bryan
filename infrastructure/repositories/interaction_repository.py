from sqlalchemy.orm import Session

from core.models.interaction import Interaction
from infrastructure.database import InteractionModel


class InteractionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_interaction(self, interaction: Interaction):
        db_interaction = InteractionModel(
            input=interaction.input,
            output=interaction.output,
            created_at=interaction.created_at,
        )
        self.db.add(db_interaction)
        self.db.commit()
        self.db.refresh(db_interaction)
        return db_interaction

    def get_interactions(self):
        return self.db.query(InteractionModel).all()
