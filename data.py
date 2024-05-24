from database import get_cv_data_with_text, get_job_description_data
from data_preprocessing import preprocess_text_nlp , match_cv_to_job
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

vectorizer = TfidfVectorizer()

def get_training_data_from_database(collaborateur_id, job_id):
    # Récupérer les données du collaborateur (CV) avec l'ID du collaborateur
    X_train = get_cv_data_with_text(collaborateur_id)
    
    # Récupérer la description du poste avec l'ID du poste
    job_description = get_job_description_data(job_id)
    
    # Prétraiter la description du poste avec spaCy
    job_description = preprocess_text_nlp(job_description)
    
    # Ajuster le vectoriseur TF-IDF avec les données d'entraînement (X_train)
    X_train_vectorized = vectorizer.fit_transform(X_train)
    
    # Transformer la description du poste
    job_description_vectorized = vectorizer.transform([job_description])
    
    # Calculer la similarité cosinus entre chaque CV et la description du poste
    y_train = [cosine_similarity(cv_vector, job_description_vectorized)[0][0] for cv_vector in X_train_vectorized]
    
    return X_train, y_train