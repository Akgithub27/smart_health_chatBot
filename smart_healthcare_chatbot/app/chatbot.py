from app.nlp import match_user_symptoms
from app.diagnosis import diagnose
from app.db import get_symptoms, get_followups_for_symptom, log_history

def start_session(session):
    session['symptom_words'] = []
    session['symptom_ids'] = []
    session['stage'] = 'collecting'
    session['followups'] = []
    session['followup_answers'] = {}
    session['followup_index'] = 0

def collect_symptoms(session, user_text):
    sym_ids, mapped = match_user_symptoms(user_text)
    entered_word = next(iter(mapped.keys())) if mapped else None
    if entered_word and entered_word not in session['symptom_words']:
        session['symptom_words'].append(entered_word)
        print("As of symptom list is : ",session['symptom_words'])
        return "Any more symptoms? Click Stop when finished."
    elif entered_word:
        return "Symptom already added. Try another."
    else:
        return "Symptom not recognized. Try another or check your spelling."

def map_symptoms_to_ids(session):
    symptom_db = get_symptoms()              # id=>name
    word2id = {v.strip().lower(): k for k, v in symptom_db.items()}
    session['symptom_ids'] = [word2id[word] for word in session['symptom_words'] if word in word2id]
    return session['symptom_ids']

def handle_stop_command(session):
    print("[STOP] symptom_words collected are:", session['symptom_words'])
    symptom_ids = map_symptoms_to_ids(session)
    print("[STOP] mapped ids:", symptom_ids)
    if not symptom_ids:
        return "Diagnosis: No symptoms provided<br>First Aid: Please enter at least one valid symptom."
    all_followups = []
    for sym_id in symptom_ids:
        followups = get_followups_for_symptom(sym_id)
        print(f"Follow-ups for symptom id {sym_id}:", followups)
        all_followups.extend(followups)
    session['followups'] = list(dict.fromkeys(all_followups))  # remove duplicates
    session['followup_index'] = 0
    if session['followups']:
        session['stage'] = 'followup'
        return session['followups'][0]
    else:
        condition, advice = diagnose(symptom_ids)
        answer = f"Diagnosis: {condition}<br>First Aid: {advice}"
        log_history(", ".join(session['symptom_words']), answer)
        session['stage'] = 'done'
        return answer

def handle_user_message(session, user_text):

    user_text_stripped = user_text.strip().lower()

    if session['stage'] == 'collecting':
        if user_text_stripped in {'done', 'stop', 'finish'}:
            return handle_stop_command(session)
        else:
            return collect_symptoms(session, user_text_stripped)

