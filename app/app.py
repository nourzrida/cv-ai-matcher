import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import os
import shutil

from model import compute_similarity
from preprocessing import preprocess
from utils import extract_basic_info, extract_text, extract_skills, extract_Projet

# 🔹 Page config
st.set_page_config(page_title="Assistant IA de Présélection de CV",
                   layout="wide")

# 🔹 Style CSS
st.markdown("""
<style>
body { background-color: #fefaf7; font-family: 'Segoe UI', sans-serif; }
.card { background-color: #fffaf7; border-radius: 20px; box-shadow: 0px 4px 20px rgba(0,0,0,0.1); padding:20px; margin-bottom:20px; }
h1 { color: #3e2723; text-align: center; font-size: 2.2rem; margin-bottom: 10px; }
h2, h3, h4 { color: #5d4037; }
.stButton>button { background: linear-gradient(135deg, #d7ccc8, #bcaaa4); color: white; border-radius: 12px; border: none; padding: 12px; font-weight: bold; width:100%; transition: 0.3s; }
.stButton>button:hover { background: linear-gradient(135deg, #bcaaa4, #8d6e63); transform: scale(1.02);}
.progress-bar { height: 12px; border-radius:6px; background: linear-gradient(90deg, #bcaaa4, #8d6e63);}
.badge { display:inline-block; padding:4px 8px; margin:2px; border-radius:8px; background-color:#d7ccc8; color:#3e2723; font-size:12px;}
</style>
""", unsafe_allow_html=True)

# 🔹 Titre
st.markdown("<div class='card'><h1>Assistant IA de Présélection de CV</h1></div>", unsafe_allow_html=True)
st.markdown("Analysez automatiquement les **CVs** par rapport à votre **offre d'emploi** et obtenez un **score de pertinence**.")

st.divider()

# 🔹 Inputs
job_offer = st.text_area("Offre d’emploi", height=150)
skills = st.text_input("Compétences clés", placeholder="Exemple : Python, Machine Learning, Data Analysis")
uploaded_files = st.file_uploader("Importer les CVs (PDF/DOC/DOCX)", type=["pdf","doc","docx"], accept_multiple_files=True)

if st.button("Lancer l’analyse"):
    if not job_offer or not skills or not uploaded_files:
        st.warning("Merci d’ajouter l'offre, les compétences et au moins un CV.")
    else:
        with st.spinner("Analyse en cours..."):
            job_processed = preprocess(job_offer)
            user_skills_list = [s.strip() for s in skills.split(",") if s.strip()]
            
            temp_dir = "./temp"
            os.makedirs(temp_dir, exist_ok=True)
            
            cv_texts = []
            file_to_name = {}
            raw_texts = {}
            
            for file in uploaded_files:
                temp_path = os.path.join(temp_dir, file.name)
                with open(temp_path, "wb") as f:
                    f.write(file.getbuffer())
                text_raw = extract_text(file)
                raw_texts[file.name] = text_raw
                parsed = extract_basic_info(text_raw)
                name = parsed.get("name", file.name)
                file_to_name[file.name] = name
                cv_texts.append(preprocess(text_raw))
            
            scores = compute_similarity(cv_texts, job_processed)
            results = sorted(zip([f.name for f in uploaded_files], scores), key=lambda x: x[1], reverse=True)

        st.success("✅ Résultats de l’analyse")

        # 🔹 Top 5 CVs
        st.markdown("<div class='card'><h2>🏆 Top 5 CVs</h2></div>", unsafe_allow_html=True)
        for filename, score in results[:5]:
            text = raw_texts[filename]
            parsed = extract_basic_info(text)
            skills_block = parsed.get("skills","")
            found_skills = extract_skills(skills_block, user_skills_list)
            skills_similarity = len(found_skills)/len(user_skills_list) if user_skills_list else 0

            # ✅ Ajout tooltip avec projets
            colored_skills = []
            for skill in user_skills_list:
                if skill in found_skills:
                    projects_for_skill = extract_Projet(skill, text)
                    tooltip_text = ", ".join(projects_for_skill) if projects_for_skill else "Aucun projet lié"
                    colored_skills.append(
                        f'<span class="badge" title="{tooltip_text}">{skill}</span>'
                    )

            st.markdown(f"<div class='card'><h3>{file_to_name[filename]}</h3>"
                        f"<p>Email: {parsed.get('email','N/A')} | Téléphone: {parsed.get('mobile_number','N/A')}</p>"
                        f"<p>Score global: {round(score*100,2)}%</p>"
                        f"<div class='progress-bar' style='width:{round(score*100,2)}%'></div>"
                        f"<p>Score compétences: {round(skills_similarity*100,2)}%</p>"
                        f"<div class='progress-bar' style='width:{round(skills_similarity*100,2)}%'></div>"
                        f"<p>Compétences correspondantes: {' '.join(colored_skills)}</p>"
                        f"</div>", unsafe_allow_html=True)

        # 🔹 Diagrammes côte à côte
        col1, col2 = st.columns(2)

        with col1:
            labels = [file_to_name[r[0]] for r in results]
            values = [round(r[1]*100,2) for r in results]
            fig, ax = plt.subplots(figsize=(5, max(3, len(labels)*0.4)))
            ax.barh(labels, values, color='#bcaaa4')
            ax.set_xlabel("Score (%)", fontsize=10, color="#5d4037")
            ax.set_title("Comparaison des CVs", fontsize=12, color="#3e2723")
            ax.invert_yaxis()
            st.pyplot(fig, use_container_width=True)

        with col2:
            all_found_skills = []
            for filename, _ in results:
                text = raw_texts[filename]
                skills_block = extract_basic_info(text).get("skills","")
                found_skills = extract_skills(skills_block, user_skills_list)
                all_found_skills.extend(found_skills)
            if all_found_skills:
                skills_count = pd.Series(all_found_skills).value_counts()
                fig2, ax2 = plt.subplots(figsize=(5,5))
                ax2.pie(skills_count.values, labels=skills_count.index, autopct='%1.1f%%',
                        colors=plt.cm.Pastel1.colors, textprops={'fontsize':9})
                ax2.set_title("Répartition des compétences", fontsize=12)
                st.pyplot(fig2, use_container_width=True)

        shutil.rmtree(temp_dir, ignore_errors=True)
