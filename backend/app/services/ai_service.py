def get_vitals_interpretation(vitals_data, patient_data, news2_score, alert_level):
    """
    Mock AI interpretation (no API needed)
    """
    
    # Extract vitals
    bp = f"{vitals_data['blood_pressure_systolic']}/{vitals_data['blood_pressure_diastolic']}"
    hr = vitals_data['heart_rate']
    temp = vitals_data['temperature']
    rr = vitals_data['respiratory_rate']
    spo2 = vitals_data['oxygen_saturation']
    
    # Generate interpretation based on NEWS2 score and vitals
    interpretations = []
    monitoring = []
    recommendations = []
    
    # Temperature analysis
    if temp > 38.0:
        interpretations.append(f"Elevated temperature ({temp}°C) indicates fever, possibly suggesting infection or inflammatory response.")
        monitoring.append("Monitor temperature every 2-4 hours")
        recommendations.append("Consider checking for infection signs (redness, warmth, pain)")
    elif temp < 36.0:
        interpretations.append(f"Low temperature ({temp}°C) may indicate hypothermia or shock.")
        monitoring.append("Monitor temperature closely and assess circulation")
    
    # Blood Pressure analysis
    if vitals_data['blood_pressure_systolic'] > 140:
        interpretations.append(f"Blood pressure {bp} mmHg is elevated above normal range.")
        monitoring.append("Monitor BP regularly")
        if patient_data.medications and 'blood pressure' not in patient_data.medications.lower():
            recommendations.append("Consider physician review for hypertension management")
    elif vitals_data['blood_pressure_systolic'] < 90:
        interpretations.append(f"Blood pressure {bp} mmHg is critically low, indicating possible hypotension or shock.")
        monitoring.append("Monitor BP every 30 minutes")
        recommendations.append("URGENT: Notify physician immediately")
    
    # Heart Rate analysis
    if hr > 100:
        interpretations.append(f"Heart rate {hr} bpm is elevated (tachycardia).")
        monitoring.append("Monitor heart rate and rhythm")
        if temp > 38.0:
            interpretations.append("Tachycardia may be related to fever.")
    elif hr < 60:
        interpretations.append(f"Heart rate {hr} bpm is below normal (bradycardia).")
        monitoring.append("Monitor heart rate closely")
        recommendations.append("Assess if patient is on beta-blockers or other rate-controlling medications")
    
    # Oxygen Saturation analysis
    if spo2 < 94:
        interpretations.append(f"Oxygen saturation {spo2}% is below optimal range.")
        monitoring.append("Monitor SpO2 continuously")
        recommendations.append("Consider supplemental oxygen and assess respiratory status")
    
    # NEWS2 Score interpretation
    if news2_score >= 7:
        recommendations.append("HIGH RISK: Immediate physician notification required")
        recommendations.append("Consider ICU/HDU transfer if condition deteriorates")
    elif news2_score >= 5:
        recommendations.append("MEDIUM RISK: Notify physician for review")
        recommendations.append("Increase monitoring frequency to every 2 hours")
    else:
        recommendations.append("Continue routine monitoring")
    
    # Patient-specific considerations
    if patient_data.allergies:
        recommendations.append(f"NOTE: Patient allergic to {patient_data.allergies} - avoid these medications")
    
    if patient_data.medications:
        recommendations.append(f"Current medications: {patient_data.medications} - consider interactions")
    
    # Build formatted response
    interpretation_text = "INTERPRETATION:\n"
    if interpretations:
        interpretation_text += "\n".join(f"• {i}" for i in interpretations)
    else:
        interpretation_text += "• Vital signs within acceptable ranges for patient age and condition."
    
    interpretation_text += "\n\nMONITORING:\n"
    if monitoring:
        interpretation_text += "\n".join(f"• {m}" for m in monitoring)
    else:
        interpretation_text += "• Continue standard monitoring protocols"
    
    interpretation_text += "\n\nRECOMMENDATIONS:\n"
    interpretation_text += "\n".join(f"• {r}" for r in recommendations)
    
    interpretation_text += "\n\n[Note: This is an automated clinical decision support tool. Always use clinical judgment and consult physician when concerned.]"
    
    return interpretation_text