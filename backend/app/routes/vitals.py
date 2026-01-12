from app.services.ai_service import get_vitals_interpretation
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.vitals import VitalSigns
from app.models.patient import Patient
from app.services.news2_calculator import calculate_news2, get_alert_level
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/api/vitals", tags=["vitals"])

# Pydantic models
class VitalsCreate(BaseModel):
    patient_id: int
    recorded_by_email: str
    blood_pressure_systolic: int
    blood_pressure_diastolic: int
    heart_rate: int
    temperature: float
    respiratory_rate: int
    oxygen_saturation: int
    weight: float = None
    notes: str = ""

class VitalsResponse(BaseModel):
    id: int
    patient_id: int
    blood_pressure_systolic: int
    blood_pressure_diastolic: int
    heart_rate: int
    temperature: float
    respiratory_rate: int
    oxygen_saturation: int
    weight: float = None
    news2_score: int
    alert_level: str
    ai_interpretation: str = None
   # ai_recommendations: str = None
    notes: str = None
    recorded_at: datetime
    recorded_by_email: str

    class Config:
        from_attributes = True

# Record new vitals
@router.post("/", response_model=VitalsResponse)
def record_vitals(vitals: VitalsCreate, db: Session = Depends(get_db)):
    print(f"=== RECORDING VITALS FOR PATIENT {vitals.patient_id} ===")
    
    # Check if patient exists
    patient = db.query(Patient).filter(Patient.id == vitals.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    print(f"Patient found: {patient.full_name}")
    
    # Calculate NEWS2 score
    vitals_dict = vitals.dict()
    news2_score = calculate_news2(vitals_dict)
    alert = get_alert_level(news2_score)
    
    print(f"NEWS2 Score: {news2_score}, Alert Level: {alert['level']}")
    
    # Get AI interpretation
    ai_interpretation = get_vitals_interpretation(
        vitals_data=vitals_dict,
        patient_data=patient,
        news2_score=news2_score,
        alert_level=alert
    )
    
    print("AI interpretation generated")
    
    # Create vitals record
    db_vitals = VitalSigns(
        **vitals_dict,
        news2_score=news2_score,
        alert_level=alert['level'],
        ai_interpretation=ai_interpretation
    )
    
    print(f"Vitals object created: {db_vitals}")
    
    # Map alert levels to patient status
    status_mapping = {
        'low': 'stable',
        'medium': 'monitoring',
        'high': 'alert'
    }
    patient.status = status_mapping.get(alert['level'], 'stable')
    
    print(f"Patient status updated to: {patient.status}")
    
    # Add both to session
    db.add(db_vitals)
    db.add(patient)
    
    print("Added to session, attempting commit...")
    
    try:
        db.commit()
        print("COMMIT SUCCESSFUL")
        db.refresh(db_vitals)
        print(f"Vitals saved with ID: {db_vitals.id}")
        
        # Verify it was actually saved
        check = db.query(VitalSigns).filter(VitalSigns.id == db_vitals.id).first()
        print(f"Verification query result: {check}")
        
    except Exception as e:
        db.rollback()
        print(f"ERROR DURING COMMIT: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to save vitals: {str(e)}")
    
    print(f"=== RETURNING VITALS ===")
    return db_vitals
# Get patient's vital history
@router.get("/patient/{patient_id}", response_model=List[VitalsResponse])
def get_patient_vitals(patient_id: int, db: Session = Depends(get_db)):
    print(f"=== FETCHING VITALS FOR PATIENT {patient_id} ===")
    
    vitals = db.query(VitalSigns).filter(
        VitalSigns.patient_id == patient_id
    ).order_by(VitalSigns.recorded_at.desc()).all()
    
    print(f"Found {len(vitals)} vitals records")
    
    return vitals

# Get single vitals record
@router.get("/{vitals_id}", response_model=VitalsResponse)
def get_vitals(vitals_id: int, db: Session = Depends(get_db)):
    vitals = db.query(VitalSigns).filter(VitalSigns.id == vitals_id).first()
    if not vitals:
        raise HTTPException(status_code=404, detail="Vitals record not found")
    return vitals