import os

import uvicorn
from fastapi import FastAPI

from app.controllers import alert_controller, interaction_controller
from infrastructure.database import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(interaction_controller.router, prefix="/api/interactions")
app.include_router(alert_controller.router, prefix="/api/alerts")

port = int(os.getenv("PORT", 8000))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=port)
