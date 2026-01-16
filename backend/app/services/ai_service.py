def get_vitals_interpretation(vitals_data, patient_data, news2_score, alert_level):
    """
    Advanced rule-based AI interpretation for vital signs.
    """
    
    # Extract vitals
    sys_bp = vitals_data['blood_pressure_systolic']
    dia_bp = vitals_data['blood_pressure_diastolic']
    hr = vitals_data['heart_rate']
    temp = vitals_data['temperature']
    rr = vitals_data['respiratory_rate']
    spo2 = vitals_data['oxygen_saturation']
    
    bp_str = f"{sys_bp}/{dia_bp}"
    
    analysis = []
    clinical_impressions = []
    recommendations = []
    
    # --- 1. PATTERN RECOGNITION (Illness Suggestions) ---
    
    # Sepsis Pattern (qSOFA-like + Temp)
    # infection signs + organ dysfunction
    sepsis_signs = 0
    if temp > 38.3 or temp < 36.0: sepsis_signs += 1
    if hr > 90: sepsis_signs += 1
    if rr > 20: sepsis_signs += 1
    if sys_bp < 100: sepsis_signs += 1
    
    if sepsis_signs >= 2:
        clinical_impressions.append("POSSIBLE SEPSIS: Multiple systematic inflammatory response signs detected.")
        recommendations.append("URGENT: Sepsis screening required (Lactate, Blood Cultures)")
        recommendations.append("Assess urine output and mental status")

    # Hypovolemic Shock Pattern
    if sys_bp < 90 and hr > 100:
        clinical_impressions.append("POSSIBLE SHOCK: Hypotension with compensatory tachycardia.")
        recommendations.append("URGENT: Assess fluid status and perfusion")
        recommendations.append("Prepare for fluid resuscitation")

    # Respiratory Failure Indicators
    if spo2 < 92 and rr > 24:
        clinical_impressions.append("RESPIRATORY DISTRESS: Hypoxia with tachypnea.")
        recommendations.append("URGENT: Respiratory assessment required")
        recommendations.append("Consider ABG and chest imaging")
        
    # Hypertensive Crisis
    if sys_bp > 180 or dia_bp > 120:
        clinical_impressions.append("HYPERTENSIVE CRISIS: Critical blood pressure elevation.")
        recommendations.append("Immediate medical review required")
        recommendations.append("Assess for end-organ damage (chest pain, headache, vision changes)")

    # Isolated findings analysis
    if temp > 38.0:
        analysis.append(f"Pyrexia ({temp}°C)")
    elif temp < 35.0:
        analysis.append(f"Hypothermia ({temp}°C)")
        
    if hr > 100:
        analysis.append(f"Tachycardia ({hr} bpm)")
    elif hr < 60:
        analysis.append(f"Bradycardia ({hr} bpm)")
        
    if spo2 < 94:
        analysis.append(f"Hypoxia ({spo2}%)")
        
    # --- 2. RISK SCORING CONTEXT ---
    
    if news2_score >= 7:
        analysis.append(f"CRITICAL NEWS2 Score ({news2_score})")
    elif news2_score >= 5:
        analysis.append(f"High NEWS2 Score ({news2_score})")

    # --- 3. PATIENT CONTEXT ---
    
    if patient_data.medications:
        # Simple interaction check (mock)
        meds = patient_data.medications.lower()
        if "beta blocker" in meds and hr < 60:
             recommendations.append("Bradycardia may be medication-induced (Beta Blockers)")
    
    # --- FORMATTING OUTPUT ---
    
    interpretation_text = ""
    
    if clinical_impressions:
        interpretation_text += "POTENTIAL CLINICAL IMPLICATIONS:\n"
        interpretation_text += "\n".join(f"⚠️ {i}" for i in clinical_impressions)
        interpretation_text += "\n\n"
        
    interpretation_text += "VITAL SIGNS ANALYSIS:\n"
    if analysis:
        interpretation_text += "\n".join(f"• {a}" for a in analysis)
    else:
        interpretation_text += "• Vital signs stable within normal limits."
    
    if recommendations:
        interpretation_text += "\n\nRECOMMENDATIONS:\n"
        interpretation_text += "\n".join(f"-> {r}" for r in recommendations)
        
    interpretation_text += "\n\n[AI SUPPORT: Validation by clinician required]"
    
    return interpretation_text