import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin",
        database="SmartHealthChatBot"
    )

def get_symptoms():
    db = get_db_connection()
    cur = db.cursor()
    cur.execute("SELECT id, symptom FROM symptoms")
    symptoms = cur.fetchall()
    cur.close()
    db.close()
    return {sym_id: sym_text for sym_id, sym_text in symptoms}

def get_symptom_synonyms():
    db = get_db_connection()
    cur = db.cursor()
    cur.execute("SELECT s.symptom, sy.synonymword FROM symptoms s JOIN synonyms sy ON s.id=sy.symptomid")
    rows = cur.fetchall()
    cur.close()
    db.close()
    synonyms = {}
    for symptom, synonym in rows:
        synonyms.setdefault(symptom, []).append(synonym)
    return synonyms

def get_followups_for_symptom(symptom_id):
    db = get_db_connection()
    cur = db.cursor()
    cur.execute("SELECT question_text FROM follow_up_questions WHERE symptomid=%s", (symptom_id,))
    questions = [row[0] for row in cur.fetchall()]
    cur.close()
    db.close()
    return questions

def get_diseases_for_symptoms(symptom_ids):
    if not symptom_ids:
        return []
    db = get_db_connection()
    cur = db.cursor()
    format_strings = ','.join(['%s'] * len(symptom_ids))
    query = f"""SELECT ds.diseaseid, d.name, COUNT(*) AS score
                FROM disease_symptom ds
                JOIN diseases d ON ds.diseaseid = d.id
                WHERE ds.symptomid IN ({format_strings})
                GROUP BY ds.diseaseid
                ORDER BY score DESC"""
    cur.execute(query, tuple(symptom_ids))
    result = cur.fetchall()
    cur.close()
    db.close()
    return result

def get_condition_advice(symptom_ids):
    db = get_db_connection()
    cur = db.cursor()
    format_strings = ','.join(['%s'] * len(symptom_ids))
    cur.execute(f"SELECT conditionsuggestion, firstaid FROM symptoms WHERE id IN ({format_strings})", tuple(symptom_ids))
    result = cur.fetchall()
    cur.close()
    db.close()
    conditions = "; ".join(r[0] for r in result if r[0])
    firstaids = "; ".join(r[1] for r in result if r[1])
    return conditions, firstaids

def log_history(userquery, botresponse):
    db = get_db_connection()
    cur = db.cursor()
    cur.execute(
        "INSERT INTO userhistory (userquery, botresponse) VALUES (%s, %s)",
        (userquery, botresponse)
    )
    db.commit()
    cur.close()
    db.close()
