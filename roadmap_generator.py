"""
roadmap_generator.py
Module 6: Skill-Gap Analysis
- Compare extracted skills with the selected role's required skills
- Show skills already found vs missing/weak skills
- Recommend a simple rule-based learning roadmap for missing skills
"""

# Very small topic-to-resource hint map for the rule-based roadmap.
LEARNING_HINTS = {
    "fastapi": "Learn FastAPI basics: routing, request/response models, docs.",
    "docker": "Learn Docker fundamentals: images, containers, Dockerfile.",
    "mlflow": "Learn MLflow for experiment tracking and model registry.",
    "cloud deployment": "Learn to deploy a model on AWS/GCP/Azure or Streamlit Cloud.",
    "sql": "Practice SQL queries: joins, aggregations, window functions.",
    "power bi": "Learn Power BI dashboards and DAX basics.",
    "transformers": "Learn Hugging Face Transformers for NLP tasks.",
    "hugging face": "Explore the Hugging Face model hub and pipelines.",
    "spacy": "Learn spaCy for NER, POS tagging, and text pipelines.",
    "opencv": "Learn OpenCV basics: image processing, contours, filters.",
    "cnn": "Study Convolutional Neural Networks for image tasks.",
    "yolo": "Learn YOLO for real-time object detection.",
    "deep learning": "Take a deep learning fundamentals course (TensorFlow/PyTorch).",
    "llm": "Learn how large language models work and prompt engineering.",
    "rag": "Learn Retrieval-Augmented Generation (RAG) architecture.",
    "apis": "Practice building and consuming REST APIs.",
    "git": "Learn Git basics: commit, branch, merge, pull requests.",
    "github": "Learn GitHub workflows and collaboration.",
}

DEFAULT_HINT = "Study the fundamentals and build one small project using this skill."


def skill_gap_analysis(found_skills: list[str], required_skills: list[str]) -> dict:
    found_set = set(s.lower().strip() for s in found_skills)
    required_set = set(s.lower().strip() for s in required_skills)

    matched = sorted(found_set & required_set)
    missing = sorted(required_set - found_set)

    return {"matched": matched, "missing": missing}


def generate_roadmap(missing_skills: list[str], weeks: int = 4) -> list[dict]:
    """
    Build a simple week-by-week roadmap covering the missing skills.
    Rule-based: one or two skills per week, cycling if there are more
    skills than weeks.
    """
    if not missing_skills:
        return [{"week": 1, "focus": "No major gaps found — polish projects and prepare for interviews."}]

    roadmap = []
    skills_per_week = max(1, -(-len(missing_skills) // weeks))  # ceil division
    for week in range(1, weeks + 1):
        chunk = missing_skills[(week - 1) * skills_per_week: week * skills_per_week]
        if not chunk:
            break
        hints = [LEARNING_HINTS.get(skill, DEFAULT_HINT) for skill in chunk]
        roadmap.append({
            "week": week,
            "skills": chunk,
            "focus": " | ".join(hints),
        })
    return roadmap


if __name__ == "__main__":
    found = ["python", "pandas", "machine learning", "scikit-learn", "sql"]
    required = ["python", "machine learning", "scikit-learn", "fastapi", "docker", "mlflow"]
    gap = skill_gap_analysis(found, required)
    print(gap)
    print(generate_roadmap(gap["missing"]))
