import sys
import os
# Ensure we can import from app
sys.path.append(os.getcwd())

from app.services.ai_service import get_vitals_interpretation

class MockPatient:
    def __init__(self, medications=None, allergies=None):
        self.medications = medications
        self.allergies = allergies

def test_ai():
    print("=== STARTING AI LOGIC VERIFICATION ===")

    # Case 1: Normal
    print("\n--- CASE 1: Normal Healthy Patient ---")
    vitals_normal = {
        'blood_pressure_systolic': 120, 'blood_pressure_diastolic': 80,
        'heart_rate': 70, 'temperature': 37.0, 'respiratory_rate': 16,
        'oxygen_saturation': 98
    }
    result = get_vitals_interpretation(vitals_normal, MockPatient(), 0, {})
    print(result)

    # Case 2: Sepsis (High Temp, High HR, High RR, Low-ish BP)
    print("\n--- CASE 2: Possible Sepsis ---")
    vitals_sepsis = {
        'blood_pressure_systolic': 95, 'blood_pressure_diastolic': 60,
        'heart_rate': 110, 'temperature': 39.0, 'respiratory_rate': 24, # Tachypnea
        'oxygen_saturation': 96
    }
    result = get_vitals_interpretation(vitals_sepsis, MockPatient(), 7, {})
    print(result)
    
    # Case 3: Hypovolemic Shock (Low BP, High HR)
    print("\n--- CASE 3: Possible Shock ---")
    vitals_shock = {
        'blood_pressure_systolic': 85, 'blood_pressure_diastolic': 50,
        'heart_rate': 125, 'temperature': 36.5, 'respiratory_rate': 22,
        'oxygen_saturation': 95
    }
    result = get_vitals_interpretation(vitals_shock, MockPatient(), 9, {})
    print(result)
    
    # Case 4: Respiratory Failure
    print("\n--- CASE 4: Respiratory Failure ---")
    vitals_resp = {
        'blood_pressure_systolic': 130, 'blood_pressure_diastolic': 85,
        'heart_rate': 90, 'temperature': 37.0, 'respiratory_rate': 30,
        'oxygen_saturation': 88
    }
    result = get_vitals_interpretation(vitals_resp, MockPatient(), 7, {})
    print(result)

if __name__ == "__main__":
    test_ai()
