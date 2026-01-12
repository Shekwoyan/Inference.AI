from sqlalchemy import Column, Integer, String, Date, Text
from app.database import Base
from datetime import date

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    hospital_number = Column(String, unique=True, index=True)  # e.g., P001
    full_name = Column(String, nullable=False)
    date_of_birth = Column(Date)
    age = Column(Integer)
    gender = Column(String)
    allergies = Column(Text, nullable=True)
    medications = Column(Text, nullable=True)
    last_visit = Column(Date, default=date.today)
    status = Column(String, default="stable")  # stable, monitoring, alert