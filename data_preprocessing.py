
import spacy

nlp = spacy.load("fr_core_news_sm")

def preprocess_text_nlp(text):
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
    return ' '.join(tokens)
