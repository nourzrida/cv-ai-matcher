from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
def compute_similarity(cv_texts, job_description):
  vectorizer = TfidfVectorizer()  # Création d'une instance
  vectors = vectorizer.fit_transform([job_description] + cv_texts).toarray()

  job_vector = vectors[0]
  cv_vectors = vectors[1:]

  cosine_similarities = cosine_similarity([job_vector], cv_vectors)
  return cosine_similarities[0]