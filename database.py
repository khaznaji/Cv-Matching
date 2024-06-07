
import pymysql
import os
from PyPDF2 import PdfReader

DB_HOST = "mysqldb"
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
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text

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
        pdf_path = os.path.join("C:\\Users\\olkhaznaji\\Desktop\\StagePFE\\Frontend\\src\\assets", pdf_path[0])
        text = extract_text_from_pdf(pdf_path)
        cv_data.append(text)
    cursor.close()
    conn.close()
    return cv_data
