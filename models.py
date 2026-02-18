from sqlalchemy import Column, Float, String, DateTime
from sqlalchemy.sql import func
from database import Base

class SpineData(Base):
    __tablename__ = "spine_data"

    id = Column(String, primary_key=True)
    patient_id = Column(String, index=True)
    upper = Column(Float)
    middle = Column(Float)
    lower = Column(Float)
    cobb = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
