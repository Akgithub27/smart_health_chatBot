"""
NLP module for symptom matching
"""
import re
from app.db import get_symptoms, get_symptom_synonyms

STOPWORDS = {"the", "and", "but", "or", "is", "a", "an", "to", "of", "have", "has", "i", "am", "my"}

def preprocess_text(text):
    """Clean and process user input text"""
    # Remove punctuation and convert to lowercase
    text = re.sub(r'[^\w\s]', '', text.lower())
    # Remove stopwords
    words = [word for word in text.split() if word not in STOPWORDS]
    # Return both the cleaned text string and word list
    return ' '.join(words), words

def match_user_symptoms(user_text):
    """
    Match user input against symptoms database
    Returns: (list of symptom IDs, dict of matched words to IDs)
    """
    # Preprocess the input
    processed_text, tokens = preprocess_text(user_text)
    print(f"[DEBUG] Original: '{user_text}' -> Processed: '{processed_text}'")
    
    # Get symptoms and synonyms from database
    symptoms = get_symptoms()  # {id: symptom_name}
    synonyms = get_symptom_synonyms()  # {symptom_name: [synonym1, synonym2]}
    
    found_ids = []
    mapped = {}  # {matched_word: symptom_id}
    
    # Check each symptom in the database
    for sym_id, sym_text in symptoms.items():
        sym_text_lower = sym_text.strip().lower()
        
        # Check if symptom name appears in the processed text
        if sym_text_lower in processed_text:
            found_ids.append(sym_id)
            mapped[sym_text_lower] = sym_id
            print(f"[DEBUG] Matched symptom: '{sym_text}' (ID: {sym_id})")
            continue
        
        # Check synonyms for this symptom
        if sym_text in synonyms:
            for syn in synonyms[sym_text]:
                syn_lower = syn.strip().lower()
                if syn_lower in processed_text:
                    found_ids.append(sym_id)
                    mapped[syn_lower] = sym_id
                    print(f"[DEBUG] Matched synonym: '{syn}' -> '{sym_text}' (ID: {sym_id})")
                    break
    
    # Remove duplicates
    found_ids = list(dict.fromkeys(found_ids))
    print(f"[DEBUG] Total matches: {len(found_ids)}")
    
    return found_ids, mapped