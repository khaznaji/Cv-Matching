from flask import Flask, request, jsonify
from transformers import BertTokenizer, BertModel
import torch
from langdetect import detect, LangDetectException
from model import get_bert_vector, cosine_similarity, initialize_vectorizer
from database import get_cv_data_with_text, get_job_description_data
from data_preprocessing import preprocess_text_nlp
import logging

# Configurer les logs
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

@app.route('/match', methods=['POST'])
def match():
    data = request.json
    collaborateur_id = data['collaborateur_id']
    job_id = data['job_id']
    
    logging.debug(f"Received request with collaborateur_id: {collaborateur_id} and job_id: {job_id}")
    
    # Obtenir les CV du collaborateur et la description du poste
    resumes = get_cv_data_with_text(collaborateur_id)
    job_description = get_job_description_data(job_id)
    
    logging.debug(f"Resumes: {resumes}")
    logging.debug(f"Job description: {job_description}")
    
    if job_description:
        try:
            # Détecter la langue de la description du poste
            job_description_lang = detect(job_description)
            logging.debug(f"Detected job description language: {job_description_lang}")
            
            # Prétraiter les CV du collaborateur
            preprocessed_resumes = []
            for resume in resumes:
                if not resume.strip():
                    logging.error("Empty resume text detected, skipping")
                    continue
                logging.debug(f"Processing resume: {resume}")
                preprocessed_resume = preprocess_text_nlp(resume)
                logging.debug(f"Preprocessed resume: {preprocessed_resume}")
                preprocessed_resumes.append(preprocessed_resume)
            
            # Vérifier que nous avons au moins un CV non vide après le prétraitement
            if not preprocessed_resumes:
                logging.error("All resumes are empty after preprocessing")
                return jsonify({"error": "All resumes are empty after preprocessing"}), 400
            
            # Prétraiter la description du poste
            logging.debug(f"Processing job description: {job_description}")
            preprocessed_job_description = preprocess_text_nlp(job_description, job_description_lang)
            logging.debug(f"Preprocessed job description: {preprocessed_job_description}")
            
            if not preprocessed_job_description.strip():
                logging.error("Job description is empty after preprocessing")
                return jsonify({"error": "Job description is empty after preprocessing"}), 400
            
            # Calculer les vecteurs BERT
            logging.debug(f"Calculating BERT vectors for resumes")
            resume_vectors = [get_bert_vector(text) for text in preprocessed_resumes]
            logging.debug(f"Calculating BERT vector for job description")
            job_description_vector = get_bert_vector(preprocessed_job_description)
            
            # Calculer la similarité cosinus entre les CV et la description du poste
            # Calculer la similarité cosinus entre les CV et la description du poste
            logging.debug(f"Calculating cosine similarity scores")
            similarity_scores = [cosine_similarity(resume_vector.reshape(1, -1), job_description_vector.reshape(1, -1))[0][0] for resume_vector in resume_vectors]

# Convert similarity_scores to Python floats
            similarity_scores = [float(score) for score in similarity_scores]

            logging.debug(f"Similarity scores: {similarity_scores}")
            return jsonify({"similarity_scores": similarity_scores})

        except LangDetectException as e:
            logging.error(f"Language detection failed: {e}")
            return jsonify({"error": "Language detection failed"}), 400
    else:
        logging.error("Job description not found")
        return jsonify({"error": "Job description not found"}), 404

if __name__ == '__main__':
    initialize_vectorizer()
    app.run(debug=True)
