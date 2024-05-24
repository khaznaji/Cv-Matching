from database import get_cv_data_with_text, get_job_description_data

# Obtenez quelques exemples de CV
collab=1
cv_data = get_cv_data_with_text(collab)
print("Exemples de CV avant le prétraitement :")
for cv in cv_data[:5]:  # Affichez seulement les 5 premiers CV pour des raisons de lisibilité
    print(cv)

# Obtenez quelques exemples de descriptions de poste
job_id = 1 
job_description_data = get_job_description_data(job_id)
print("\nExemples de descriptions de poste avant le prétraitement :")
for description in job_description_data[:5]:  # Affichez seulement les 5 premières descriptions de poste
    print(description)
