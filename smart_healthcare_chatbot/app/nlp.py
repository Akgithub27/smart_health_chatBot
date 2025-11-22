import re
from app.db import get_symptoms, get_symptom_synonyms

STOPWORDS = {"the", "and", "but", "or", "is", "a", "an", "to", "of", "have", "has"}

def preprocess_text(text):
    text = re.sub(r'[^\w\s]', '', text.lower())
    return [word for word in text.split() if word not in STOPWORDS]

def match_user_symptoms(user_text):
    user_tokens = preprocess_text(user_text)
    symptoms = get_symptoms()
    synonyms = get_symptom_synonyms()
    found_ids = []
    mapped = {}
    for sym_id, sym_text in symptoms.items():
        # match main symptom
        if sym_text.lower() in user_tokens:
            found_ids.append(sym_id)
            mapped[sym_text] = sym_id
        # match all synonyms for this symptom
        elif sym_text in synonyms:
            for syn in synonyms[sym_text]:
                if syn.lower() in user_tokens:
                    found_ids.append(sym_id)
                    mapped[syn] = sym_id
    # Deduplicate
    found_ids = list(set(found_ids))
    return found_ids, mapped
