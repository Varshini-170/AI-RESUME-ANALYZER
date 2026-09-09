"""
app.py
Module 7: Streamlit Dashboard
- Resume upload section
- Target-role selection
- Extracted skills display
- Match-score chart
- Recommended job roles
- Missing skills and learning roadmap
- Downloadable analysis report
"""

import os
import tempfile
import pandas as pd
import streamlit as st
import plotly.express as px

from resume_parser import validate_file, extract_resume_text
from text_cleaner import clean_text
from skill_extractor import load_skill_dictionary, extract_skills
from job_matcher import load_job_roles, match_resume_to_roles, top_n_roles
from roadmap_generator import skill_gap_analysis, generate_roadmap

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")

st.title("📄 AI Resume Analyzer and Job Recommendation System")
st.caption(
    "Upload your resume to get a match score, missing skills, and a simple "
    "learning roadmap. This tool is for guidance only — not automatic hiring "
    "or rejection."
)

# ---- Module 4: Load reference datasets ----
skill_dict = load_skill_dictionary("data/skill_dictionary.csv")
job_roles = load_job_roles("data/job_roles.csv")

# ---- Module 1: Resume Upload ----
st.header("1. Upload Your Resume")
uploaded_file = st.file_uploader("Upload a PDF or DOCX resume", type=["pdf", "docx"])

store_resume = st.checkbox(
    "Allow temporary storage of this resume for this session only", value=True
)

if uploaded_file is not None:
    st.success(f"File uploaded: {uploaded_file.name}")

    # Save to a temp file for parsing (Responsible AI: temp only, deleted after use)
    suffix = os.path.splitext(uploaded_file.name)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.getbuffer())
        tmp_path = tmp.name

    is_valid, message = validate_file(tmp_path)

    if not is_valid:
        st.error(message)
    else:
        # ---- Module 2: Text Extraction and Cleaning ----
        raw_text = extract_resume_text(tmp_path)
        cleaned_text = clean_text(raw_text)

        # ---- Module 3: Skill Extraction ----
        skills_result = extract_skills(cleaned_text, skill_dict)
        found_skills = skills_result["flat"]

        st.header("2. Extracted Skills")
        if found_skills:
            st.write(f"Found **{len(found_skills)}** skills in your resume.")
            for category, skills in skills_result["by_category"].items():
                st.markdown(f"**{category.replace('_', ' ').title()}**: {', '.join(sorted(set(skills)))}")
        else:
            st.warning("No known skills detected. Try a resume with more explicit technical keywords.")

        # ---- Module 5: Matching and Recommendation ----
        st.header("3. Target Role & Match Scores")
        target_role = st.selectbox("Select your target role", job_roles["job_role"].tolist())

        ranked = match_resume_to_roles(cleaned_text, job_roles)

               
        bar_colors = [
            "#2CA02C" if role == target_role else "#1f77b4"
            for role in ranked["job_role"]
        ]

        fig = px.bar(
            ranked, x="job_role", y="match_score",
            labels={"job_role": "Job Role", "match_score": "Match Score (%)"},
            title=f"Resume Match Score by Job Role (target: {target_role})",
            text="match_score",
        )
        fig.update_traces(marker_color=bar_colors)
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Top 3 Recommended Roles")
        top3 = top_n_roles(ranked, 3)
        for i, row in top3.iterrows():
            st.write(f"{i+1}. **{row['job_role']}** — {row['match_score']}%")

        # ---- Module 6: Skill-Gap Analysis + Roadmap ----
        st.header("4. Skill Gap & Learning Roadmap")
        role_row = job_roles[job_roles["job_role"] == target_role].iloc[0]
        required_skills = [s.strip() for s in role_row["required_skills"].split(",")]

        gap = skill_gap_analysis(found_skills, required_skills)

        col1, col2 = st.columns(2)
        with col1:
            st.success("✅ Skills you already have")
            st.write(", ".join(gap["matched"]) if gap["matched"] else "None matched yet.")
        with col2:
            st.error("❌ Missing / weak skills")
            st.write(", ".join(gap["missing"]) if gap["missing"] else "No gaps — great fit!")

        roadmap = generate_roadmap(gap["missing"])
        st.subheader("Suggested 4-Week Roadmap")
        for week in roadmap:
            label = f"Week {week['week']}"
            if "skills" in week:
                label += f": {', '.join(week['skills'])}"
            st.markdown(f"**{label}**")
            st.write(week["focus"])

        # ---- Downloadable report ----
        st.header("5. Download Report")
        target_score = ranked[ranked["job_role"] == target_role]["match_score"].values[0]
        report_lines = [
            f"AI Resume Analyzer Report",
            f"Target Role: {target_role}",
            f"Match Score: {target_score}%",
            "",
            "Skills Found:",
            *[f"- {s}" for s in found_skills],
            "",
            "Missing Skills:",
            *[f"- {s}" for s in gap["missing"]],
            "",
            "Recommended Roles:",
            *[f"{i+1}. {r['job_role']} - {r['match_score']}%" for i, r in top3.iterrows()],
            "",
            "Suggested Roadmap:",
            *[f"Week {w['week']}: {w['focus']}" for w in roadmap],
        ]
        report_text = "\n".join(report_lines)
        st.download_button(
            "Download Analysis Report (.txt)",
            data=report_text,
            file_name="resume_analysis_report.txt",
            mime="text/plain",
        )

        # Responsible AI reminder
        st.caption("⚠️ Match scores are estimates based on text similarity, not hiring decisions.")

    # Clean up temp file
    try:
        os.remove(tmp_path)
    except OSError:
        pass
else:
    st.info("👆 Upload a resume to get started.")
