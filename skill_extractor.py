"""
skill_extractor.py
Module 3: Skill Extraction
- Load a controlled list of technical/job-related skills
- Search the resume for those skills (keyword matching, beginner approach)
- Group skills into categories such as programming, databases, ML, cloud, tools
"""

import re
import pandas as pd
from text_cleaner import clean_text


def load_skill_dictionary(csv_path: str = "data/skill_dictionary.csv") -> pd.DataFrame:
    return pd.read_csv(csv_path)


def extract_skills(cleaned_resume_text: str, skill_df: pd.DataFrame) -> dict:
    """
    Search cleaned resume text for each skill in the dictionary.
    Uses word-boundary matching so 'r' doesn't match inside 'grow', etc.
    Returns a dict grouped by category: {category: [skills]}
    """
    found_by_category = {}
    found_flat = []

    for _, row in skill_df.iterrows():
        skill = str(row["skill"]).lower().strip()
        category = str(row["category"]).strip()

        # Build a safe regex pattern; skills like c++ / c# need escaping
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"
        if re.search(pattern, cleaned_resume_text):
            found_flat.append(skill)
            found_by_category.setdefault(category, []).append(skill)

    return {
        "flat": sorted(set(found_flat)),
        "by_category": found_by_category,
    }


if __name__ == "__main__":
    sample_text = "Experienced in Python, Pandas, SQL, Docker and Machine Learning projects."
    cleaned = clean_text(sample_text)
    skills_df = load_skill_dictionary()
    result = extract_skills(cleaned, skills_df)
    print(result)
