import os
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from dotenv import load_dotenv

# 1. SETUP: Load API Key
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

def get_vitals_interpretation(vitals_data, patient_data, news2_score, alert_level):
    """
    MAIN FUNCTION:
    Tries to get a smart AI response using the 'latest' alias. 
    If it fails, it falls back to your custom rule-based logic.
    """
    
    # Prepare Data for AI Prompt
    patient_info = f"{patient_data.age} year old {patient_data.gender}"
    meds = patient_data.medications if patient_data.medications else "None"
    allergies = patient_data.allergies if patient_data.allergies else "None"
    
    prompt = f"""
    You are an expert Clinical Decision Support System. 
    Analyze the following patient data and write a short, professional clinical assessment.
    
    PATIENT: {patient_info}
    HISTORY: Meds: {meds} | Allergies: {allergies}
    
    VITALS:
    - HR: {vitals_data['heart_rate']} bpm
    - BP: {vitals_data['blood_pressure_systolic']}/{vitals_data['blood_pressure_diastolic']} mmHg
    - Temp: {vitals_data['temperature']} C
    - RR: {vitals_data['respiratory_rate']} /min
    - SpO2: {vitals_data['oxygen_saturation']}%
    
    NEWS2 SCORE: {news2_score} (Risk Level: {alert_level['level'].upper()})
    
    INSTRUCTIONS:
    - Start with a 1-sentence summary of the patient's stability.
    - Highlight specific vital signs that are abnormal.
    - Provide 2-3 actionable nursing recommendations.
    - Use Markdown formatting (bolding, bullet points) for readability.
    - Be concise (max 150 words).
    """

    try:
        if not GOOGLE_API_KEY:
            raise Exception("No API Key found")

        # 2. Configure Model
        # We use 'gemini-flash-latest' because it appeared explicitly in your check_models.py list
        model = genai.GenerativeModel('gemini-flash-latest')
        
        # 3. SAFETY SETTINGS: Turn OFF filters
        safety_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }

        # 4. Call Google AI
        response = model.generate_content(prompt, safety_settings=safety_settings)
        
        if response.text:
            return response.text
        else:
            raise Exception("Empty response from AI")

    except Exception as e:
        print(f"AI Service Unavailable ({str(e)}). Using Heuristic Fallback.")
        return _generate_fallback_text(vitals_data, patient_data, news2_score, alert_level)

def _generate_fallback_text(vitals_data, patient_data, news2_score, alert_level):
    """
    FALLBACK ENGINE:
    Runs your custom rule-based logic when AI is unavailable.
    """
    
    # Extract variables
    bp = f"{vitals_data['blood_pressure_systolic']}/{vitals_data['blood_pressure_diastolic']}"
    hr = vitals_data['heart_rate']
    temp = vitals_data['temperature']
    spo2 = vitals_data['oxygen_saturation']
    
    # Initialize lists
    interpretations = []
    monitoring = []
    recommendations = []
    
    # --- YOUR LOGIC ---
    
    # Temperature
    if temp > 38.0:
        interpretations.append(f"Elevated temperature ({temp}°C) indicates fever.")
        monitoring.append("Monitor temperature every 2-4 hours")
    elif temp < 36.0:
        interpretations.append(f"Low temperature ({temp}°C) - assess for hypothermia.")
        
    # Blood Pressure
    if vitals_data['blood_pressure_systolic'] > 140:
        interpretations.append(f"BP {bp} is elevated.")
    elif vitals_data['blood_pressure_systolic'] < 90:
        interpretations.append(f"BP {bp} is critically low (Hypotension).")
        recommendations.append("URGENT: Notify physician immediately")
        
    # Heart Rate
    if hr > 100:
        interpretations.append(f"Tachycardia detected ({hr} bpm).")
    elif hr < 60:
        interpretations.append(f"Bradycardia detected ({hr} bpm).")
        
    # Oxygen
    if spo2 < 94:
        interpretations.append(f"Hypoxia detected (SpO2 {spo2}%).")
        recommendations.append("Consider supplemental oxygen")

    # NEWS2 Risk
    if news2_score >= 7:
        recommendations.append("HIGH RISK: Immediate response required.")
    elif news2_score >= 5:
        recommendations.append("MEDIUM RISK: Urgent review required.")

    # --- FORMAT OUTPUT ---
    text = "### **Automated Fallback Assessment**\n\n"
    
    if interpretations:
        text += "**Observations:**\n" + "\n".join(f"- {i}" for i in interpretations) + "\n\n"
    else:
        text += "Vital signs are within normal ranges.\n\n"
    
    if monitoring:
        text += "**Monitoring Plan:**\n" + "\n".join(f"- {m}" for m in monitoring) + "\n\n"
        
    if recommendations:
        text += "**Recommendations:**\n" + "\n".join(f"- {r}" for r in recommendations)
    
    return text