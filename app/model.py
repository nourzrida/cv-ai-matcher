from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def compute_similarity(cv_texts, job_description):
    vectorizer = TfidfVectorizer()
    vectorizer.fit([job_description])
    job_vector = vectorizer.transform([job_description])
    cv_vectors = vectorizer.transform(cv_texts)
    cosine_similarities = cosine_similarity(job_vector, cv_vectors)
    return cosine_similarities[0]
