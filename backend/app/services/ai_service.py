import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Debug line
print(f"API Key loaded: {os.getenv('GOOGLE_API_KEY')[:10]}...")

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def get_vitals_interpretation(vitals_data, patient_data, news2_score, alert_level):
    """
    Get AI interpretation using Google Gemini
    """
    
    prompt = f"""You are a clinical decision support assistant helping nurses interpret vital signs.

VITAL SIGNS DATA:
- Blood Pressure: {vitals_data['blood_pressure_systolic']}/{vitals_data['blood_pressure_diastolic']} mmHg
- Heart Rate: {vitals_data['heart_rate']} bpm
- Temperature: {vitals_data['temperature']}°C
- Respiratory Rate: {vitals_data['respiratory_rate']} breaths/min
- Oxygen Saturation: {vitals_data['oxygen_saturation']}%
- NEWS2 Score: {news2_score} ({alert_level['text']})

PATIENT CONTEXT:
- Name: {patient_data.full_name}
- Age: {patient_data.age} years
- Gender: {patient_data.gender}
- Known Allergies: {patient_data.allergies or 'None'}
- Current Medications: {patient_data.medications or 'None'}

TASK:
Provide a brief clinical interpretation for the nurse:
1. What these vitals might indicate (without diagnosing)
2. What to monitor closely
3. Whether doctor notification is recommended
4. Any relevant considerations given the patient's context

CRITICAL CONSTRAINTS:
- You are a decision SUPPORT tool, not a decision MAKER
- NEVER provide specific diagnoses
- NEVER prescribe treatments or medications
- Use phrases like "may indicate", "consider", "warrants evaluation"
- Always recommend physician involvement for concerning patterns
- Keep response under 200 words
- Use clear, professional language

FORMAT YOUR RESPONSE AS:
INTERPRETATION:
[Your interpretation here]

MONITORING:
[What to monitor]

RECOMMENDATIONS:
[Action items for nurse]
"""

    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash-exp',
            contents=prompt
        )
        return response.text
        
    except Exception as e:
        print(f"AI Service Error: {e}")
        return "AI interpretation temporarily unavailable. Please use clinical judgment and consult with physician if needed."