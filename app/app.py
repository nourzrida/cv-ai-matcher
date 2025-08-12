import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image
from model import compute_similarity
from preprocessing import preprocess
from utils import extract_text

st.set_page_config(
    page_title="Assistant IA de Présélection de CV",
    page_icon="🧠",
    layout="centered",
)
st.title("🧠 Assistant IA de Présélection de CV")
st.markdown(
    """
    Bienvenue dans l’assistant IA qui compare automatiquement les **CVs** à votre **offre d’emploi**  
    et calcule un **score de pertinence** pour vous aider à présélectionner les meilleurs profils.
    """
)

st.divider() 
job_offer = st.text_area(
    "📄 **Offre d’emploi :**",
    placeholder="Collez ici la description complète du poste...",
    height=200
)

uploaded_files = st.file_uploader(
    "📂 **Importer les CVs (PDF)**",
    type=["pdf", "doc"],
    accept_multiple_files=True,
    help="Vous pouvez importer plusieurs CVs à la fois"
)

if st.button("🚀 Lancer l’analyse", type="primary"):
    if not job_offer or not uploaded_files:
        st.warning("⚠️ Merci d’ajouter **une offre d’emploi** et au moins **un CV**.")
    else:
        with st.spinner("🔄 Analyse en cours..."):
            # Prétraitement de l'offre
            job_processed = preprocess(job_offer)

            cv_texts, filenames = [], []
            for file in uploaded_files:
                text = extract_text(file)
                processed = preprocess(text)
                cv_texts.append(processed)
                filenames.append(file.name)

            scores = compute_similarity(cv_texts, job_processed)

            # Fusion nom + score, tri décroissant
            results = sorted(zip(filenames, scores), key=lambda x: x[1], reverse=True)
        st.success("✅ **Résultats de l’analyse :**")

        for filename, score in results:
            pourcentage = score * 100
            st.markdown(
                f"📁 **{filename}** — Pertinence : `{pourcentage:.2f}%`"
            )

        fig, ax = plt.subplots()
        ax.barh([r[0] for r in results], [r[1] * 100 for r in results], color="#4CAF50")
        ax.set_xlabel("Score de pertinence (%)")
        ax.set_title("Comparaison des CVs")
        st.pyplot(fig)
