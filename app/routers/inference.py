from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Vital
from ..schemas import InferenceRequest, InferenceResult

router = APIRouter(prefix="/inference", tags=["inference"])

# Simple rule-based inference engine


@router.post("/", response_model=InferenceResult)
def run_inference(payload: InferenceRequest, db: Session = Depends(get_db)):
    vital = db.query(Vital).get(payload.vital_id)
    if not vital:
        raise HTTPException(status_code=404, detail="Vital record not found")

    symptoms = []
    possible_illnesses = []

    # Rule-based checks (basic medical logic)
    if vital.temperature and vital.temperature > 38.0:
        symptoms.append("Fever")
        possible_illnesses.append("Infection")

    if vital.heart_rate and vital.heart_rate > 100:
        symptoms.append("Tachycardia")
        possible_illnesses.append("Anxiety, Dehydration, or Cardiac issue")

    if vital.systolic_bp and vital.systolic_bp > 140:
        symptoms.append("High blood pressure")
        possible_illnesses.append("Hypertension")

    if vital.oxygen_saturation and vital.oxygen_saturation < 92:
        symptoms.append("Low oxygen saturation")
        possible_illnesses.append("Respiratory condition")

    if not symptoms:
        symptoms.append("No abnormal findings")
        possible_illnesses.append("Healthy")

    return InferenceResult(
        symptoms=symptoms,
        possible_illnesses=possible_illnesses,
        evidence="Rule-based checks on vital signs"
    )
