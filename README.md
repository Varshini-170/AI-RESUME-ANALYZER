# AI Resume Analyzer and Job Recommendation System

A Streamlit app that reads your resume (PDF or DOCX), compares it against a
set of job roles, and shows you a match score, your top 3 recommended
roles, missing skills, and a simple learning roadmap.

**Live app:** https://ai-resume-analyzer-slrivthbphwx3h4jbvyhyx.streamlit.app/
*(hosted on Streamlit Community Cloud — may take a few seconds to wake up if it's been idle)*

## What it does

- Upload a PDF or DOCX resume
- Extracts and cleans the text
- Detects skills using a keyword list
- Scores your resume against 7 job roles (TF-IDF + cosine similarity)
- Shows your top 3 matching roles on a chart
- Shows missing skills for your target role + a 4-week roadmap
- Lets you download a text report of the results

## How it works
Upload resume -> Extract text -> Clean text -> Find skills
-> Compare with job roles -> Score + rank roles
-> Show missing skills + roadmap -> Streamlit dashboard

## Folder Structure

ai_resume_analyzer/
|-- app.py # Streamlit dashboard
|-- resume_parser.py # File upload + text extraction
|-- text_cleaner.py # Text cleaning
|-- skill_extractor.py # Skill detection
|-- job_matcher.py # Matching + ranking
|-- roadmap_generator.py # Skill gaps + roadmap
|-- requirements.txt
|-- data/ # job_roles.csv, skill_dictionary.csv
|-- sample_resumes/ # Sample resumes to test with
|-- tests/ # test_cases.csv


## How to run it

```bash
git clone <your-repo-url>
cd ai_resume_analyzer
pip install -r requirements.txt
streamlit run app.py
```

Then open the link it prints (usually `http://localhost:8501`) and upload a
resume from `sample_resumes/` to try it out.

## Note-
- This is a guidance tool, not a hiring decision-maker. It doesn't look at
  gender, age, religion, nationality, or anything like that — only skills
  and text similarity.
- Match scores are estimates. A missing keyword doesn't always mean a
  missing skill.
- Uploaded resumes are processed temporarily and deleted right after —
  nothing is stored permanently.
