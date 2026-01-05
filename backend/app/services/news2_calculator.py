def calculate_news2(vitals):
    """Calculate NEWS2 score from vital signs"""
    score = 0
    
    # Respiratory Rate
    rr = vitals.get('respiratory_rate', 0)
    if rr <= 8:
        score += 3
    elif 9 <= rr <= 11:
        score += 1
    elif 21 <= rr <= 24:
        score += 2
    elif rr >= 25:
        score += 3
    
    # Oxygen Saturation
    spo2 = vitals.get('oxygen_saturation', 0)
    if spo2 <= 91:
        score += 3
    elif 92 <= spo2 <= 93:
        score += 2
    elif 94 <= spo2 <= 95:
        score += 1
    
    # Temperature
    temp = vitals.get('temperature', 0)
    if temp <= 35.0:
        score += 3
    elif 35.1 <= temp <= 36.0:
        score += 1
    elif 38.1 <= temp <= 39.0:
        score += 1
    elif temp >= 39.1:
        score += 2
    
    # Blood Pressure (Systolic)
    bp_sys = vitals.get('blood_pressure_systolic', 0)
    if bp_sys <= 90:
        score += 3
    elif 91 <= bp_sys <= 100:
        score += 2
    elif 101 <= bp_sys <= 110:
        score += 1
    elif bp_sys >= 220:
        score += 3
    
    # Heart Rate
    hr = vitals.get('heart_rate', 0)
    if hr <= 40:
        score += 3
    elif 41 <= hr <= 50:
        score += 1
    elif 91 <= hr <= 110:
        score += 1
    elif 111 <= hr <= 130:
        score += 2
    elif hr >= 131:
        score += 3
    
    return score

def get_alert_level(score):
    """Determine alert level from NEWS2 score"""
    if score >= 7:
        return {
            'level': 'high',
            'color': 'red',
            'text': 'High Risk - Urgent Medical Attention Required'
        }
    elif score >= 5:
        return {
            'level': 'medium',
            'color': 'yellow',
            'text': 'Medium Risk - Monitor Closely'
        }
    else:
        return {
            'level': 'low',
            'color': 'green',
            'text': 'Low Risk - Stable'
        }