
import docx2txt
import PyPDF2

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
