import streamlit as st
from model import compute_similarity
from preprocessing import preprocess
from utils import extract_text

st.title("🧠 Assistant IA de Présélection de CV")

job_offer = st.text_area("📄 Offre d’emploi :", height=200)

uploaded_files = st.file_uploader("📂 Importer les CVs ", type="pdf", accept_multiple_files=True)

if st.button("Lancer l’analyse"):
    if not job_offer or not uploaded_files:
        st.warning("Merci d’ajouter une offre d’emploi et des CVs.")
    else:
        st.info("🔄 Traitement en cours...")

        # Prétraitement de l'offre
        job_processed = preprocess(job_offer)

        cv_texts = []
        filenames = []

        for file in uploaded_files:
            text = extract_text(file)
            processed = preprocess(text)
            cv_texts.append(processed)
            filenames.append(file.name)

        # Calcul des similarités
        scores = compute_similarity(cv_texts, job_processed)

        # Fusion nom de fichier + score et tri décroissant
        results = sorted(zip(filenames, scores), key=lambda x: x[1], reverse=True)

        # Affichage
        st.success("✅ Résultats :")
        for filename, score in results:
            pourcentage = score * 100
            st.write(f"📁 {filename} — Pertinence : `{pourcentage:.2f}%`")
