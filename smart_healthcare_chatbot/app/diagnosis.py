from app.db import get_diseases_for_symptoms, get_condition_advice

def diagnose(symptom_ids):
    if not symptom_ids:
        return "No symptoms provided", "Please enter at least one symptom."
    diseases = get_diseases_for_symptoms(symptom_ids)
    if diseases:
        disease_name = diseases[0][1]
    else:
        disease_name = "Unknown Condition"
    conditions, firstaid = get_condition_advice(symptom_ids)
    return f"{disease_name} ({conditions})", firstaid
