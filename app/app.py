import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import os
import shutil
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from model import compute_similarity
from preprocessing import preprocess
from utils import extract_basic_info, extract_text, extract_skills, extract_Projet

st.set_page_config(
    page_title="Assistant IA de Présélection de CV",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    
    .main {
        padding-top: 2rem;
    }
    
    .stApp {
        background: linear-gradient(135deg, #fefaf7 0%, #fff8f0 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #8d6e63 0%, #5d4037 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        color: #f5f5f5;
        font-size: 1.1rem;
        margin-top: 0.5rem;
        opacity: 0.9;
    }
    
    /* Card styling */
    .custom-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid rgba(141, 110, 99, 0.1);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .custom-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
    }
    
    /* Input styling */
    .stTextArea textarea, .stTextInput input {
        border-radius: 12px !important;
        border: 2px solid #e0e0e0 !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #8d6e63 !important;
        box-shadow: 0 0 0 3px rgba(141, 110, 99, 0.1) !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #8d6e63 0%, #5d4037 100%);
        color: white;
        border-radius: 12px;
        border: none;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(141, 110, 99, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #6d4c41 0%, #3e2723 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(141, 110, 99, 0.4);
    }
    
    /* Progress bars */
    .progress-container {
        background-color: #f5f5f5;
        border-radius: 10px;
        height: 8px;
        margin: 0.5rem 0;
        overflow: hidden;
    }
    
    .progress-bar {
        height: 100%;
        border-radius: 10px;
        background: linear-gradient(90deg, #8d6e63, #5d4037);
        transition: width 0.8s ease;
        position: relative;
    }
    
    .progress-bar::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        animation: shimmer 2s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    /* Skill badges */
    .skill-badge {
        display: inline-block;
        padding: 0.4rem 0.8rem;
        margin: 0.2rem;
        border-radius: 20px;
        background: linear-gradient(135deg, #d7ccc8, #bcaaa4);
        color: #3e2723;
        font-size: 0.85rem;
        font-weight: 500;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: transform 0.2s ease;
    }
    
    .skill-badge:hover {
        transform: scale(1.05);
    }
    
    .skill-badge.matched {
        background: linear-gradient(135deg, #4caf50, #388e3c);
        color: white;
    }
    
    /* Results section */
    .result-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border-left: 4px solid #8d6e63;
        transition: all 0.3s ease;
    }
    
    .result-card:hover {
        transform: translateX(5px);
        box-shadow: 0 6px 25px rgba(0,0,0,0.12);
    }
    
    .candidate-name {
        font-size: 1.3rem;
        font-weight: 600;
        color: #3e2723;
        margin-bottom: 0.5rem;
    }
    
    .candidate-info {
        color: #666;
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }
    
    .score-display {
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f8f4f0;
    }
    
    /* Metrics styling */
    .metric-container {
        background: white;
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #8d6e63;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #666;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>🎯 Assistant IA de Présélection de CV</h1>
    <p>Analysez automatiquement les CVs par rapport à votre offre d'emploi et obtenez un score de pertinence intelligent</p>
</div>
""", unsafe_allow_html=True)
with st.sidebar:
    st.markdown("### ⚙️ Paramètres d'analyse")
    
    similarity_threshold = st.slider(
        "Seuil de similarité minimum (%)",
        min_value=0,
        max_value=100,
        value=30,
        help="CVs avec un score inférieur ne seront pas affichés"
    )  
    max_results = st.selectbox(
        "Nombre maximum de résultats",
        options=[5, 10, 15, 20],
        index=0
    )
    
    show_charts = st.checkbox("Afficher les graphiques", value=True)
    show_detailed_skills = st.checkbox("Analyse détaillée des compétences", value=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown("### 📝 Description du poste")
    job_offer = st.text_area(
        "Décrivez le poste et les exigences",
        height=150,
        placeholder="Exemple: Nous recherchons un développeur Python avec 3+ ans d'expérience en machine learning..."
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown("### 🎯 Compétences clés")
    skills = st.text_area(
        "Compétences recherchées (séparées par des virgules)",
        height=150,
        placeholder="Python, Machine Learning, TensorFlow, SQL, Git"
    )
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="custom-card">', unsafe_allow_html=True)
st.markdown("### 📁 Import des CVs")
uploaded_files = st.file_uploader(
    "Glissez-déposez vos fichiers CV ici",
    type=["pdf", "doc", "docx"],
    accept_multiple_files=True,
    help="Formats supportés: PDF, DOC, DOCX"
)
if uploaded_files:
    st.success(f"✅ {len(uploaded_files)} fichier(s) importé(s)")
    
st.markdown('</div>', unsafe_allow_html=True)
if st.button("🚀 Lancer l'analyse ", type="primary"):
    if not job_offer or not skills or not uploaded_files:
        st.error("⚠️ Merci de remplir tous les champs et d'importer au moins un CV.")
    else:

        progress_bar = st.progress(0)
        status_text = st.empty()
        
        with st.spinner("🔍 Analyse en cours..."):
            status_text.text("Traitement de l'offre d'emploi...")
            progress_bar.progress(10)
            job_processed = preprocess(job_offer)
            user_skills_list = [s.strip() for s in skills.split(",") if s.strip()]
            temp_dir = "./temp"
            os.makedirs(temp_dir, exist_ok=True) 
            cv_texts = []
            file_to_name = {}
            raw_texts = {}
            for i, file in enumerate(uploaded_files):
                status_text.text(f"Traitement du CV {i+1}/{len(uploaded_files)}: {file.name}")
                progress_bar.progress(20 + (i * 60 // len(uploaded_files)))
                
                temp_path = os.path.join(temp_dir, file.name)
                with open(temp_path, "wb") as f:
                    f.write(file.getbuffer())
                text_raw = extract_text(file)
                raw_texts[file.name] = text_raw
                parsed = extract_basic_info(text_raw)
                name = parsed.get("name", file.name)
                file_to_name[file.name] = name
                cv_texts.append(preprocess(text_raw))
            
            # Compute similarities
            status_text.text("Calcul des scores de similarité...")
            progress_bar.progress(85)
            scores = compute_similarity(cv_texts, job_processed)
            results = sorted(zip([f.name for f in uploaded_files], scores), key=lambda x: x[1], reverse=True)
            
            # Filter by threshold
            filtered_results = [(f, s) for f, s in results if s * 100 >= similarity_threshold]
            
            progress_bar.progress(100)
            status_text.text("✅ Analyse terminée!")
            
        st.balloons()
        
        # 🔹 Results summary
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-value">{len(filtered_results)}</div>
                <div class="metric-label">CVs qualifiés</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            avg_score = sum(s for _, s in filtered_results) / len(filtered_results) if filtered_results else 0
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-value">{avg_score*100:.1f}%</div>
                <div class="metric-label">Score moyen</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            best_score = max(s for _, s in filtered_results) if filtered_results else 0
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-value">{best_score*100:.1f}%</div>
                <div class="metric-label">Meilleur score</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col4:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-value">{len(user_skills_list)}</div>
                <div class="metric-label">Compétences recherchées</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # 🔹 Top candidates
        st.markdown("## 🏆 Candidats recommandés")
        
        display_count = min(max_results, len(filtered_results))
        
        for i, (filename, score) in enumerate(filtered_results[:display_count]):
            text = raw_texts[filename]
            parsed = extract_basic_info(text)
            skills_block = parsed.get("skills", "")
            found_skills = extract_skills(skills_block, user_skills_list)
            skills_similarity = len(found_skills) / len(user_skills_list) if user_skills_list else 0

            # Create skill badges with project tooltips
            skill_badges = []
            for skill in user_skills_list:
                if skill in found_skills:
                    projects_for_skill = extract_Projet(skill, text)
                    tooltip_text = ", ".join(projects_for_skill) if projects_for_skill else "Aucun projet lié"
                    skill_badges.append(
                        f'<span class="skill-badge matched" title="{tooltip_text}">{skill} ✓</span>'
                    )
                else:
                    skill_badges.append(f'<span class="skill-badge">{skill}</span>')

            # Rank badge
            rank_emoji = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else f"#{i+1}"
            
            st.markdown( f"<div class='result-card'>"
    f"<div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;'>"
    f"<div class='candidate-name'>{rank_emoji} {file_to_name[filename]}</div>"
    f"<div style='font-size: 1.2rem; font-weight: 600; color: #8d6e63;'>{score*100:.1f}%</div>"
    f"</div>"

    f"<p class='candidate-info'>📧 {parsed.get('email','N/A')} | 📱 {parsed.get('mobile_number','N/A')}</p>"

    f"<div style='margin-bottom: 1rem;'>"
    f"<div class='score-display' style='color: #8d6e63;'>📊 Score global: {score*100:.1f}%</div>"
    f"<div class='progress-container'><div class='progress-bar' style='width:{score*100:.1f}%'></div></div>"
    f"</div>"

    f"<div style='margin-bottom: 1rem;'>"
    f"<div class='score-display' style='color: #4caf50;'>🎯 Compétences correspondantes: {skills_similarity*100:.1f}%</div>"
    f"<div class='progress-container'><div class='progress-bar' style='width:{skills_similarity*100:.1f}%; background: linear-gradient(90deg,#4caf50,#388e3c);'></div></div>"
    f"</div>"

    f"<div><strong>Compétences:</strong><br>{' '.join(skill_badges)}</div>"
    f"</div>",
    unsafe_allow_html=True
)
        if show_charts and filtered_results:
            st.markdown("## 📊 Analyse visuelle")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Interactive bar chart with Plotly
                names = [file_to_name[r[0]] for r in filtered_results[:10]]
                scores_pct = [r[1]*100 for r in filtered_results[:10]]
                
                fig = go.Figure(data=[
                    go.Bar(
                        x=scores_pct,
                        y=names,
                        orientation='h',
                        marker=dict(
                            color=scores_pct,
                            colorscale='RdYlBu_r',
                            showscale=True,
                            colorbar=dict(title="Score (%)")
                        ),
                        text=[f"{s:.1f}%" for s in scores_pct],
                        textposition='inside'
                    )
                ])
                
                fig.update_layout(
                    title="🏆 Classement des candidats",
                    xaxis_title="Score (%)",
                    yaxis_title="Candidats",
                    height=400,
                    template="plotly_white"
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                all_found_skills = []
                for filename, _ in filtered_results:
                    text = raw_texts[filename]
                    skills_block = extract_basic_info(text).get("skills", "")
                    found_skills = extract_skills(skills_block, user_skills_list)
                    all_found_skills.extend(found_skills)
                
                if all_found_skills:
                    skills_count = pd.Series(all_found_skills).value_counts()
                    
                    fig2 = go.Figure(data=[
                        go.Pie(
                            labels=skills_count.index,
                            values=skills_count.values,
                            hole=0.4,
                            marker=dict(
                                colors=px.colors.qualitative.Set3
                            )
                        )
                    ])
                    
                    fig2.update_layout(
                        title="🎯 Répartition des compétences",
                        height=400,
                        template="plotly_white"
                    )
                    
                    st.plotly_chart(fig2, use_container_width=True)
        shutil.rmtree(temp_dir, ignore_errors=True)


