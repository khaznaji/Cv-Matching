import pymysql
import os
import fitz  # PyMuPDF
import logging

DB_HOST = "localhost"
DB_USER = "root"
DB_NAME = "pfe"

def get_job_description_data(job_id):
    conn = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        db=DB_NAME
    )
    
    with conn.cursor() as cursor:
        cursor.execute("SELECT description FROM poste WHERE id = %s", (job_id,))
        job_description = cursor.fetchone()

    conn.close()
    return job_description[0] if job_description else None

def extract_text_from_pdf(pdf_path):
    try:
        with fitz.open(pdf_path) as doc:
            text = ''
            for page in doc:
                text += page.get_text()
        return text
    except Exception as e:
        logging.error(f"Error extracting text from PDF: {e}")
        return ''

def get_cv_data_with_text(collaborateur_id):
    conn = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        db=DB_NAME
    )
    cursor = conn.cursor()
    cursor.execute("SELECT resume FROM Collaborateur WHERE id = %s", (collaborateur_id,))
    cv_data = []
    for pdf_path in cursor.fetchall():
        pdf_path = os.path.join("C:\\Users\\DELL\\Desktop\\pfe\\StagePFE_Front\\src\\assets", pdf_path[0])
        text = extract_text_from_pdf(pdf_path)
        if text.strip():  # Vérifier si le texte extrait n'est pas vide
            cv_data.append(text)
        else:
            logging.error(f"Empty text extracted from PDF: {pdf_path}")
    cursor.close()
    conn.close()
    return cv_data
