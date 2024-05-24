
from flask import Flask, request, jsonify
from model import get_job_description_vector, vectorizer, cosine_similarity
from database import get_cv_data_with_text
from data_preprocessing import preprocess_text_nlp  # Importez preprocess_text_nlp


app = Flask(__name__)

@app.route('/match', methods=['POST'])
def match():
    data = request.json
    collaborateur_id = data['collaborateur_id']
    job_id = data['job_id']
    
    # Obtenir les CV du collaborateur et la description du poste
    resumes = get_cv_data_with_text(collaborateur_id)
    job_description = get_job_description_vector(job_id)
    
    if job_description is not None:
        # Prétraiter les CV du collaborateur et la description du poste
        preprocessed_resumes = [preprocess_text_nlp(resume) for resume in resumes]
        preprocessed_job_description = preprocess_text_nlp(job_description)
        
        # Transformer les textes en vecteurs TF-IDF
        resume_vectors = vectorizer.transform(preprocessed_resumes)
        job_description_vector = vectorizer.transform([preprocessed_job_description])
        
        # Calculer la similarité cosinus entre les CV et la description du poste
        similarity_scores = cosine_similarity(resume_vectors, job_description_vector)
        
        # Convertir les scores de similarité en liste pour le retour JSON
        similarity_scores_list = similarity_scores.ravel().tolist()
        
        return jsonify({"similarity_scores": similarity_scores_list})
    else:
        return jsonify({"error": "Job description not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
