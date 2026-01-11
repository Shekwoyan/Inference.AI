from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Vital, Patient
from ..schemas import VitalCreate, VitalOut

# Create a router for vital-related endpoints
router = APIRouter(prefix="/vitals", tags=["vitals"])

# Record new vital signs for a patient


@router.post("/", response_model=VitalOut)
def record_vital(payload: VitalCreate, db: Session = Depends(get_db)):
    # Check if patient exists
    patient = db.query(Patient).get(payload.patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Create vital record
    vital = Vital(**payload.dict())
    db.add(vital)
    db.commit()
    db.refresh(vital)
    return vital

# Get a vital record by ID


@router.get("/{vital_id}", response_model=VitalOut)
def get_vital(vital_id: int, db: Session = Depends(get_db)):
    vital = db.query(Vital).get(vital_id)
    if not vital:
        raise HTTPException(status_code=404, detail="Vital not found")
    return vital
