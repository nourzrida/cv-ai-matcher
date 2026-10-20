# 🎯 CV AI Matcher

Application Streamlit en français pour présélectionner automatiquement des CV en fonction d'une offre d'emploi et de compétences recherchées.

L'application extrait le texte des CV, le prétraite avec spaCy, calcule un score de similarité TF-IDF/cosinus et affiche les candidats les plus pertinents avec leurs compétences correspondantes.

## ✨ Fonctionnalités

- Analyse d'une description de poste et d'une liste de compétences clés
- Import de plusieurs CV au format PDF, DOC ou DOCX
- Extraction automatique du texte des CV
- Extraction des informations principales : nom, e-mail, téléphone et compétences
- Calcul d'un score de similarité entre chaque CV et l'offre d'emploi
- Filtrage des résultats selon un seuil de similarité configurable
- Affichage des meilleurs candidats avec classement et score
- Analyse des compétences correspondantes
- Graphiques interactifs avec Plotly
- Interface utilisateur personnalisée avec Streamlit

## 🗂️ Structure du projet

```text
cv-ai-matcher/
├── app/
│   ├── app.py             # Interface Streamlit et logique principale
│   ├── model.py           # Calcul de similarité TF-IDF/cosinus
│   ├── preprocessing.py   # Nettoyage, lemmatisation et suppression des stop words
│   └── utils.py           # Extraction du texte et des informations des CV
└── README.md
```

## 🛠️ Technologies utilisées

- Python 3.9+
- Streamlit
- spaCy (`fr_core_news_md`)
- scikit-learn
- PyPDF2
- docx2txt
- pandas
- Plotly
- Matplotlib

## 🚀 Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/nourzrida/cv-ai-matcher.git
cd cv-ai-matcher
```

### 2. Créer un environnement virtuel

```bash
python -m venv .venv
```

Activez l'environnement virtuel :

**Linux/macOS**

```bash
source .venv/bin/activate
```

**Windows PowerShell**

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Installer les dépendances

```bash
pip install streamlit spacy scikit-learn PyPDF2 docx2txt pandas plotly matplotlib
```

### 4. Installer le modèle spaCy français

```bash
python -m spacy download fr_core_news_md
```

## ▶️ Lancer l'application

Depuis la racine du projet :

```bash
streamlit run app/app.py
```

L'application sera accessible à l'adresse affichée par Streamlit, généralement :

```text
http://localhost:8501
```

## 📖 Utilisation

1. Saisissez la description du poste.
2. Ajoutez les compétences recherchées en les séparant par des virgules.
3. Importez un ou plusieurs CV au format PDF, DOC ou DOCX.
4. Configurez le seuil minimal de similarité et le nombre maximal de résultats.
5. Cliquez sur **Lancer l'analyse**.
6. Consultez le classement, les scores, les compétences détectées et les graphiques.

Exemple de compétences :

```text
Python, Machine Learning, TensorFlow, SQL, Git
```

## 🧠 Méthode de scoring

Le score est calculé en deux étapes :

1. Le texte de l'offre et les CV sont nettoyés, lemmatisés et débarrassés des mots vides avec spaCy.
2. La similarité cosinus est calculée entre le vecteur TF-IDF de l'offre et celui de chaque CV.

Le score affiché est compris entre 0 % et 100 %. Il s'agit d'un indicateur automatique d'aide à la présélection et non d'une décision de recrutement.

## ⚠️ Limites connues

- Les CV scannés ou composés uniquement d'images peuvent nécessiter une reconnaissance optique de caractères (OCR).
- La qualité des résultats dépend de l'extraction du texte et de la formulation de l'offre.
- L'extraction des sections de compétences et de projets repose sur des formats de CV relativement structurés.
- Le modèle spaCy `fr_core_news_md` doit être installé avant le démarrage.
- Les scores ne remplacent pas l'évaluation humaine et doivent être utilisés comme support à la décision.

## 🔒 Données et confidentialité

Les CV sont traités localement par l'application pendant l'analyse. Vérifiez votre configuration de déploiement et vos obligations légales avant d'utiliser des données personnelles de candidats en production.

## 📄 Licence

Aucune licence open source n'est actuellement définie dans ce dépôt. Ajoutez un fichier `LICENSE` si vous souhaitez préciser les conditions d'utilisation et de distribution du projet.
