"""
Diagnosis generation module
"""
from app.db import get_diseases_for_symptoms, get_condition_advice

def diagnose(symptom_ids):
    """
    Generate diagnosis based on symptom IDs
    Returns: (condition_string, firstaid_string)
    """
    if not symptom_ids:
        return "No symptoms provided", "Please enter at least one symptom."
    
    print(f"[DEBUG] Generating diagnosis for symptom IDs: {symptom_ids}")
    
    # Find matching diseases
    diseases = get_diseases_for_symptoms(symptom_ids)
    
    if diseases:
        disease_id, disease_name, score = diseases[0]
        print(f"[DEBUG] Top match: {disease_name} (score: {score})")
        
        # Show alternatives if available
        if len(diseases) > 1:
            alternatives = [d[1] for d in diseases[1:3]]
            disease_name += f" (Also consider: {', '.join(alternatives)})"
    else:
        disease_name = "Unknown Condition"
        print("[DEBUG] No matching diseases found")
    
    # Get condition suggestions and first aid
    conditions, firstaid = get_condition_advice(symptom_ids)
    
    # Format output
    if conditions:
        full_condition = f"{disease_name} - {conditions}"
    else:
        full_condition = disease_name
    
    if not firstaid:
        firstaid = "Please consult a healthcare professional for proper diagnosis and treatment."
    
    print(f"[DEBUG] Diagnosis: {full_condition}")
    return full_condition, firstaid