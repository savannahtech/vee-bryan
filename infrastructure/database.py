import os

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_name = os.getenv("SQLALCHEMY_DATABASE", "deepchecks.db")

SQLALCHEMY_DATABASE_URL = f"sqlite:///./{db_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class InteractionModel(Base):
    __tablename__ = "interactions"
    id = Column(Integer, primary_key=True, index=True)
    input = Column(String)
    output = Column(String)
    created_at = Column(DateTime)


class MetricModel(Base):
    __tablename__ = "metrics"
    id = Column(Integer, primary_key=True, index=True)
    interaction_id = Column(Integer, ForeignKey("interactions.id"))
    input_metric = Column(Float)
    output_metric = Column(Float)


class AlertModel(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, index=True)
    interaction_id = Column(Integer, ForeignKey("interactions.id"))
    element = Column(String)
    metric_value = Column(Float)
    alert_type = Column(String)
    created_at = Column(DateTime)


Base.metadata.create_all(bind=engine)
