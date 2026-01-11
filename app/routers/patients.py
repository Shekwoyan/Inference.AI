from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Patient
from ..schemas import PatientCreate, PatientOut

# Create a router for patient-related endpoints
router = APIRouter(prefix="/patients", tags=["patients"])

# Create a new patient


@router.post("/", response_model=PatientOut)
def create_patient(payload: PatientCreate, db: Session = Depends(get_db)):
    patient = Patient(**payload.dict())
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient

# Get a patient by ID


@router.get("/{patient_id}", response_model=PatientOut)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).get(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient
