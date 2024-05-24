
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from database import get_job_description_data, get_cv_data_with_text
from data_preprocessing import preprocess_text_nlp

# Initialisation de la vectorisation
vectorizer = TfidfVectorizer(max_features=1000)

def initialize_vectorizer():
    collaborateur_id = 1
    resumes = get_cv_data_with_text(collaborateur_id)
    job_descriptions = []
    for job_id in range(1, 100):
        job_description = get_job_description_data(job_id)
        if job_description:
            job_descriptions.append(job_description)
    
    # Prétraitement des données avec spaCy
    resumes = [preprocess_text_nlp(resume) for resume in resumes]
    job_descriptions = [preprocess_text_nlp(desc) for desc in job_descriptions]

    # Ajustement du vectorizer sur les données prétraitées
    global vectorizer
    vectorizer.fit(resumes + job_descriptions)

def get_job_description_vector(job_id):
    job_description = get_job_description_data(job_id)
    if job_description:
        # Prétraitement de la description du poste avec spaCy
        return preprocess_text_nlp(job_description)
    return None

initialize_vectorizer()
