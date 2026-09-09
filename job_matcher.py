"""
job_matcher.py
Module 5: Matching and Recommendation
- Convert resume and job descriptions into comparable text vectors (TF-IDF)
- Calculate cosine similarity
- Rank roles from highest to lowest score
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_job_roles(csv_path: str = "data/job_roles.csv") -> pd.DataFrame:
    return pd.read_csv(csv_path)


def match_resume_to_roles(cleaned_resume_text: str, job_roles_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compare the resume against each job role's required-skills text
    using TF-IDF + cosine similarity. Returns a DataFrame ranked by
    match score (highest first).
    """
    role_texts = job_roles_df["required_skills"].str.replace(",", " ").tolist()
    documents = [cleaned_resume_text] + role_texts

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)

    resume_vector = tfidf_matrix[0:1]
    role_vectors = tfidf_matrix[1:]

    scores = cosine_similarity(resume_vector, role_vectors).flatten()

    results = job_roles_df.copy()
    results["match_score"] = (scores * 100).round(1)
    results = results.sort_values("match_score", ascending=False).reset_index(drop=True)
    return results


def top_n_roles(ranked_df: pd.DataFrame, n: int = 3) -> pd.DataFrame:
    return ranked_df.head(n)


if __name__ == "__main__":
    from text_cleaner import clean_text

    resume = "Python developer skilled in pandas numpy machine learning scikit-learn sql"
    cleaned = clean_text(resume)
    roles = load_job_roles()
    ranked = match_resume_to_roles(cleaned, roles)
    print(ranked[["job_role", "match_score"]])
