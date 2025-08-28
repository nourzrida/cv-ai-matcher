
import docx2txt
import PyPDF2
import re

def extract_text_from_pdf(uploaded_file):
    text = ""
    reader = PyPDF2.PdfReader(uploaded_file)  # Pas besoin de open()
    for page in reader.pages:
        text += page.extract_text()
    return text
def extract_text_from_txt(file):
 with open(file, "r",encoding="utf-8") as f:
   return f.read()
def extract_text_from_docs(file):
  return docx2txt.process(file)
def extract_text(file):
    filename = file.name.lower()
    if filename.endswith('.pdf'):
        return extract_text_from_pdf(file)
    elif filename.endswith('.docx') or filename.endswith('.doc'):
        return extract_text_from_docs(file)
  
    else:
        return "Format non pris en charge"

def extract_basic_info(text):
    email = re.findall(r'\S+@\S+', text)
    phone = re.findall(r'\+?\d[\d\s]{6,}\d', text)
    name = text.strip().split("\n")[0] if text.strip() else "N/A"
    skills_match = re.search(
        r'COMP[ÉE]TENCES\s*(.*?)(?:\n[A-ZÉÈÊÂÎÔÙÛÇ ]{3,}\n|$)', 
        text,  re.DOTALL
    )
    
    projects_match = re.search(
        r'(PROJETS|EXPÉRIENCES ACADÉMIQUES)\s*(.*?)(?:\n[A-ZÉÈÊÂÎÔÙÛÇ ]{3,}\n|$)', 
        text,  re.DOTALL
    )
    project_text = projects_match.group(2).strip() if projects_match else ""
    skills_text = skills_match.group(1).strip() if skills_match else ""
    skills_list = []
    for line in skills_text.split("\n"):
        clean_skill = re.sub(r'^[\-\*\•\s]+', '', line).strip()  # supprime puces/tirets
        if clean_skill:
            skills_list.append(clean_skill)
    return {
        "name": name,
        "email": email[0] if email else "N/A",
        "mobile_number": phone[0] if phone else "N/A",
        "skills": skills_text,
        "projects": project_text
    }

def extract_skills(text, skills_list):
    skills_found = []
    text_lower = text.lower()
    for skill in skills_list :
        if skill.lower().strip() in text_lower:
            skills_found.append(skill.strip())
    return skills_found
def extract_Projet(skill, text):
    parsed = extract_basic_info(text) 
    projet_list = []

    projects_text = parsed.get("projects", "")
    if not projects_text:
        return projet_list  
    all_projects = [p.strip() for p in projects_text.split(",") if p.strip()]
    for proj in all_projects:
        if skill.lower() in proj.lower():
            projet_list.append(proj)

    return projet_list

