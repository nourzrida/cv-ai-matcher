import spacy
import re

nlp = spacy.load("fr_core_news_md")

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = text.lower()
    return text

def preprocess(text):
    doc = nlp(clean_text(text))
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return " ".join(tokens)
