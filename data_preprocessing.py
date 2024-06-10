import spacy
from langdetect import detect, LangDetectException

# Charger les modèles spaCy
nlp_fr = spacy.load("fr_core_news_sm")
nlp_en = spacy.load("en_core_web_sm")

def preprocess_text_nlp(text, lang=None):
    if not text.strip():  # Vérifie si le texte est vide ou contient seulement des espaces
        return ""
    
    if lang is None:
        try:
            lang = detect(text)
        except LangDetectException:
            lang = 'en'  # Défaut à l'anglais si la langue ne peut pas être détectée

    if lang == 'fr':
        doc = nlp_fr(text)
    else:
        doc = nlp_en(text)
    
    tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
    return ' '.join(tokens)
