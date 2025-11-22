"""
Database operations module
"""
import mysql.connector

def get_db_connection():
    """Create and return database connection"""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin",
        database="smarthealthchatbot"
    )

def get_symptoms():
    """
    Fetch all symptoms from database
    Returns: dict {symptom_id: symptom_name}
    """
    db = get_db_connection()
    cur = db.cursor()
    cur.execute("SELECT id, symptom FROM symptoms")
    symptoms = cur.fetchall()
    cur.close()
    db.close()
    return {sym_id: sym_text.strip() for sym_id, sym_text in symptoms}

def get_symptom_synonyms():
    """
    Fetch symptom synonyms from database
    Returns: dict {symptom_name: [synonym1, synonym2, ...]}
    """
    db = get_db_connection()
    cur = db.cursor()
    cur.execute("""
        SELECT s.symptom, sy.synonymword 
        FROM symptoms s 
        JOIN synonyms sy ON s.id = sy.symptomid
    """)
    rows = cur.fetchall()
    cur.close()
    db.close()
    
    synonyms = {}
    for symptom, synonym in rows:
        symptom = symptom.strip()
        synonym = synonym.strip()
        synonyms.setdefault(symptom, []).append(synonym)
    
    return synonyms

def get_followups_for_symptom(symptom_id):
    """
    Get follow-up questions for a specific symptom
    Returns: list of question strings
    """
    db = get_db_connection()
    cur = db.cursor()
    cur.execute(
        "SELECT question_text FROM follow_up_questions WHERE symptomid = %s",
        (symptom_id,)
    )
    questions = [row[0] for row in cur.fetchall()]
    cur.close()
    db.close()
    print(f"[DEBUG] Found {len(questions)} follow-up questions for symptom ID {symptom_id}")
    return questions

def get_diseases_for_symptoms(symptom_ids):
    """
    Find diseases matching the given symptoms
    Returns: list of tuples (disease_id, disease_name, match_score)
    """
    if not symptom_ids:
        return []
    
    db = get_db_connection()
    cur = db.cursor()
    
    placeholders = ','.join(['%s'] * len(symptom_ids))
    query = f"""
        SELECT ds.diseaseid, d.name, COUNT(*) AS score
        FROM disease_symptom ds
        JOIN diseases d ON ds.diseaseid = d.id
        WHERE ds.symptomid IN ({placeholders})
        GROUP BY ds.diseaseid, d.name
        ORDER BY score DESC
    """
    
    cur.execute(query, tuple(symptom_ids))
    result = cur.fetchall()
    cur.close()
    db.close()
    
    return result

def get_condition_advice(symptom_ids):
    """
    Get condition suggestions and first aid for symptoms
    Returns: (conditions_string, firstaid_string)
    """
    if not symptom_ids:
        return "", ""
    
    db = get_db_connection()
    cur = db.cursor()
    
    placeholders = ','.join(['%s'] * len(symptom_ids))
    query = f"""
        SELECT conditionsuggestion, firstaid 
        FROM symptoms 
        WHERE id IN ({placeholders})
    """
    
    cur.execute(query, tuple(symptom_ids))
    result = cur.fetchall()
    cur.close()
    db.close()
    
    conditions = "; ".join(r[0] for r in result if r[0])
    firstaids = "; ".join(r[1] for r in result if r[1])
    
    return conditions, firstaids

def log_history(userquery, botresponse):
    """Log conversation history to database"""
    db = get_db_connection()
    cur = db.cursor()
    cur.execute(
        "INSERT INTO userhistory (userquery, botresponse) VALUES (%s, %s)",
        (userquery, botresponse)
    )
    db.commit()
    cur.close()
    db.close()