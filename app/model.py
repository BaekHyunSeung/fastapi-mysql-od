from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.sql import func
from app.database import Base

class DetectionResult(Base):
    __tablename__ = "detection_results"

    id = Column(Integer, primary_key=True, index=True)
    image_name = Column(String(255))
    label = Column(String(100))
    confidence = Column(Float)
    bbox = Column(JSON)
    created_at = Column(DateTime(timezone=True), default=func.now())
