from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# -------------------
# Patient Schemas
# -------------------


class PatientCreate(BaseModel):
    name: str
    age: Optional[int] = None
    gender: Optional[str] = None
    notes: Optional[str] = ""


class PatientOut(BaseModel):
    id: int
    name: str
    age: Optional[int]
    gender: Optional[str]
    notes: Optional[str]

    class Config:
        from_attributes = True  # allows ORM objects to be converted to Pydantic

# -------------------
# Vital Schemas
# -------------------


class VitalCreate(BaseModel):
    patient_id: int
    heart_rate: Optional[float] = None
    systolic_bp: Optional[float] = None
    diastolic_bp: Optional[float] = None
    temperature: Optional[float] = None
    respiratory_rate: Optional[float] = None
    oxygen_saturation: Optional[float] = None
    timestamp: Optional[datetime] = None


class VitalOut(VitalCreate):
    id: int

    class Config:
        from_attributes = True

# -------------------
# Inference Schemas
# -------------------


class InferenceRequest(BaseModel):
    vital_id: int


class InferenceResult(BaseModel):
    symptoms: List[str]
    possible_illnesses: List[str]
    evidence: Optional[str] = None
