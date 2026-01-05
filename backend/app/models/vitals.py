from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class VitalSigns(Base):
    __tablename__ = "vital_signs"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    recorded_by_email = Column(String)  # Nurse who recorded it
    
    # Vital measurements
    blood_pressure_systolic = Column(Integer)
    blood_pressure_diastolic = Column(Integer)
    heart_rate = Column(Integer)
    temperature = Column(Float)
    respiratory_rate = Column(Integer)
    oxygen_saturation = Column(Integer)
    weight = Column(Float, nullable=True)
    
    # Calculated scores
    news2_score = Column(Integer)
    alert_level = Column(String)  # low, medium, high
    
    # AI interpretation
    ai_interpretation = Column(Text, nullable=True)
    ai_recommendations = Column(Text, nullable=True)
    
    # Metadata
    notes = Column(Text, nullable=True)
    recorded_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    patient = relationship("Patient", backref="vital_signs")