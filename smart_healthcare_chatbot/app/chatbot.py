"""
Core chatbot conversation logic
"""
from app.nlp import match_user_symptoms
from app.diagnosis import diagnose
from app.db import get_symptoms, get_followups_for_symptom, log_history

def start_session(session):
    """Initialize a new chat session"""
    session['symptom_words'] = []
    session['symptom_ids'] = []
    session['stage'] = 'collecting'
    session['followups'] = []
    session['followup_answers'] = {}
    session['followup_index'] = 0
    print("[DEBUG] New session started")

def collect_symptoms(session, user_text):
    """
    Process user symptom input during collection stage
    """
    # Match symptoms in user input
    sym_ids, mapped = match_user_symptoms(user_text)
    
    if not mapped:
        print(f"[DEBUG] No symptoms recognized in: {user_text}")
        return "Symptom not recognized. Please try another symptom or check your spelling."
    
    # Get the matched symptom name
    entered_word = next(iter(mapped.keys()))
    
    # Check if symptom already added
    if entered_word in session['symptom_words']:
        print(f"[DEBUG] Duplicate symptom: {entered_word}")
        return "This symptom has already been added. Please enter another symptom."
    
    # Add new symptom
    session['symptom_words'].append(entered_word)
    print(f"[DEBUG] Symptom added: {entered_word}")
    print(f"[DEBUG] Current symptoms: {session['symptom_words']}")
    
    return "Symptom recorded. Any more symptoms? Click 'Stop' when finished."

def map_symptoms_to_ids(session):
    """Map collected symptom names to database IDs"""
    symptom_db = get_symptoms()  # {id: name}
    word2id = {v.strip().lower(): k for k, v in symptom_db.items()}
    
    session['symptom_ids'] = [
        word2id[word] 
        for word in session['symptom_words'] 
        if word in word2id
    ]
    
    print(f"[DEBUG] Mapped symptom IDs: {session['symptom_ids']}")
    return session['symptom_ids']

def handle_stop_command(session):
    """
    Handle when user finishes entering symptoms
    Transitions to follow-up questions or diagnosis
    """
    print(f"[DEBUG] STOP - Collected symptoms: {session['symptom_words']}")
    
    # Map symptom names to IDs
    symptom_ids = map_symptoms_to_ids(session)
    
    if not symptom_ids:
        return "No valid symptoms provided. Please enter at least one symptom and try again."
    
    # Gather all follow-up questions for the symptoms
    all_followups = []
    for sym_id in symptom_ids:
        followups = get_followups_for_symptom(sym_id)
        print(f"[DEBUG] Symptom ID {sym_id}: {len(followups)} follow-up(s)")
        all_followups.extend(followups)
    
    # Remove duplicate questions
    session['followups'] = list(dict.fromkeys(all_followups))
    session['followup_index'] = 0
    
    print(f"[DEBUG] Total unique follow-up questions: {len(session['followups'])}")
    
    # If there are follow-up questions, ask the first one
    if session['followups']:
        session['stage'] = 'followup'
        first_question = session['followups'][0]
        print(f"[DEBUG] Asking first follow-up question: {first_question}")
        return f"<b>Follow-up Question 1 of {len(session['followups'])}:</b><br>{first_question}"
    
    # No follow-ups, proceed directly to diagnosis
    print("[DEBUG] No follow-up questions, proceeding to diagnosis")
    condition, advice = diagnose(symptom_ids)
    answer = f"<b>Diagnosis:</b> {condition}<br><br><b>First Aid:</b> {advice}"
    
    log_history(", ".join(session['symptom_words']), answer)
    session['stage'] = 'done'
    
    return answer

def handle_followup_response(session, user_text):
    """Handle user's response to follow-up questions"""
    current_index = session['followup_index']
    
    if current_index >= len(session['followups']):
        return "All questions answered."
    
    # Store the answer
    current_question = session['followups'][current_index]
    session['followup_answers'][current_question] = user_text
    print(f"[DEBUG] Answer recorded for Q{current_index + 1}: {user_text}")
    
    # Move to next question
    session['followup_index'] += 1
    
    # Check if more questions remain
    if session['followup_index'] < len(session['followups']):
        next_question = session['followups'][session['followup_index']]
        question_num = session['followup_index'] + 1
        total = len(session['followups'])
        print(f"[DEBUG] Asking question {question_num} of {total}")
        return f"<b>Follow-up Question {question_num} of {total}:</b><br>{next_question}"
    
    # All questions answered, provide diagnosis
    print("[DEBUG] All follow-up questions answered")
    condition, advice = diagnose(session['symptom_ids'])
    answer = f"<b>Diagnosis:</b> {condition}<br><br><b>First Aid:</b> {advice}"
    
    log_history(", ".join(session['symptom_words']), answer)
    session['stage'] = 'done'
    
    return answer

def handle_user_message(session, user_text):
    """
    Main message handler - routes to appropriate function based on stage
    """
    user_text_stripped = user_text.strip().lower()
    current_stage = session.get('stage', 'collecting')
    
    print(f"[DEBUG] Stage: {current_stage}, Message: {user_text}")
    
    # Collecting symptoms stage
    if current_stage == 'collecting':
        if user_text_stripped in {'done', 'stop', 'finish'}:
            return handle_stop_command(session)
        else:
            return collect_symptoms(session, user_text)
    
    # Follow-up questions stage
    elif current_stage == 'followup':
        return handle_followup_response(session, user_text)
    
    # Session completed
    else:
        return "Session finished. Click the reset button to start a new consultation."