from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

# Patient table


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer)
    gender = Column(String)
    notes = Column(Text, default="")

    # Relationship to vitals
    vitals = relationship("Vital", back_populates="patient",
                          cascade="all, delete-orphan")

# Vital signs table


class Vital(Base):
    __tablename__ = "vitals"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    heart_rate = Column(Float)
    systolic_bp = Column(Float)
    diastolic_bp = Column(Float)
    temperature = Column(Float)
    respiratory_rate = Column(Float)
    oxygen_saturation = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationship back to patient
    patient = relationship("Patient", back_populates="vitals")
