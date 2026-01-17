from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.patient import Patient
from pydantic import BaseModel
from datetime import date

router = APIRouter(prefix="/api/patients", tags=["patients"])

# Pydantic models for request/response
class PatientCreate(BaseModel):
    hospital_number: str
    full_name: str
    date_of_birth: date
    age: int
    gender: str
    allergies: str = ""
    medications: str = ""

class PatientResponse(BaseModel):
    id: int
    hospital_number: str
    full_name: str
    age: int
    gender: str
    last_visit: date
    status: str

    class Config:
        from_attributes = True

# Get all patients
@router.get("/", response_model=List[PatientResponse])
def get_patients(db: Session = Depends(get_db)):
    patients = db.query(Patient).all()
    return patients

# Search patients
@router.get("/search", response_model=List[PatientResponse])
def search_patients(q: str, db: Session = Depends(get_db)):
    patients = db.query(Patient).filter(
        (Patient.hospital_number.contains(q)) | 
        (Patient.full_name.contains(q))
    ).all()
    return patients

# Get single patient
@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

# Create new patient
@router.post("/", response_model=PatientResponse)
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    # Check if hospital number already exists
    existing = db.query(Patient).filter(
        Patient.hospital_number == patient.hospital_number
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Hospital number already exists")
    
    db_patient = Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient
