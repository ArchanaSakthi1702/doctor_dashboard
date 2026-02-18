from pydantic import BaseModel
from datetime import datetime

class SpineDataCreate(BaseModel):
    patient_id: str
    upper: float
    middle: float
    lower: float
    cobb: float
