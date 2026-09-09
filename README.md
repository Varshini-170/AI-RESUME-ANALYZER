# AI Resume Analyzer and Job Recommendation System

An NLP-based Streamlit application that analyzes a resume (PDF/DOCX), scores it
against a set of job roles, identifies missing skills, and generates a simple
learning roadmap.

## Features

- Upload PDF or DOCX resumes
- Automatic text extraction and cleaning
- Skill extraction using a controlled skill dictionary (keyword matching)
- Resume-to-role matching using **TF-IDF + cosine similarity**
- Top-3 role recommendations with a match-score chart
- Skill-gap analysis (matched vs. missing skills)
- Rule-based 4-week learning roadmap
- Downloadable text analysis report
- Responsible-AI guardrails: no protected attributes are scored, and match
  scores are explicitly labeled as estimates, not hiring decisions

## Architecture / Workflow

```
Upload PDF or DOCX resume
        |
Extract resume text        (resume_parser.py)
        |
Clean and normalize text   (text_cleaner.py)
        |
Identify skills            (skill_extractor.py)
        |
Load job-role requirements (data/job_roles.csv)
        |
Compare resume with roles  (job_matcher.py — TF-IDF + cosine similarity)
        |
Calculate match scores
        |
Recommend top roles
        |
Show missing skills + roadmap (roadmap_generator.py)
        |
Streamlit dashboard        (app.py)
```

## Folder Structure

```
ai_resume_analyzer/
|-- app.py                  # Streamlit dashboard (Module 7)
|-- resume_parser.py        # Upload validation + text extraction (Modules 1-2)
|-- text_cleaner.py         # Text cleaning/normalization (Module 2)
|-- skill_extractor.py      # Skill extraction (Module 3)
|-- job_matcher.py          # TF-IDF matching + ranking (Module 5)
|-- roadmap_generator.py    # Skill-gap analysis + roadmap (Module 6)
|-- requirements.txt
|-- README.md
|-- .env
|-- .gitignore
|
|-- data/
|   |-- job_roles.csv       # Job roles + required skills (Module 4)
|   |-- skill_dictionary.csv
|
|-- sample_resumes/         # Sample resumes for testing (no real personal data)
|
|-- reports/                # Generated analysis reports (gitignored)
|
|-- tests/
    |-- test_cases.csv      # Testing & evaluation sheet (Module 11)
```

## Setup

1. **Clone and enter the project folder**
   ```bash
   git clone <your-repo-url>
   cd ai_resume_analyzer
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**
   ```bash
   streamlit run app.py
   ```

5. Open the URL Streamlit prints (usually `http://localhost:8501`) and upload
   a resume from `sample_resumes/` to try it out.

## How Matching Works (Beginner Approach)

1. Resume text and each job role's required-skills string are converted into
   TF-IDF vectors.
2. Cosine similarity is computed between the resume vector and each role
   vector.
3. Roles are ranked by similarity score (0–100%).
4. The top 3 roles are shown as recommendations.

This is the "beginner approach" from the project spec. For an "advanced"
version, swap `TfidfVectorizer` in `job_matcher.py` for **Sentence
Transformers** embeddings (semantic matching) — the rest of the pipeline
stays the same.

## Extending the Project (Optional Advanced Features)

- Resume section detection (education / skills / projects / experience)
- Job-description upload instead of only predefined roles
- LLM-generated resume feedback (Groq / Gemini / OpenAI) via a controlled prompt
- FastAPI backend + Docker deployment
- User login and saved reports (would need a database — SQLite/PostgreSQL)
- Downloadable PDF report (currently `.txt`)

## Responsible AI Notes

- This tool is for **guidance only**, not automatic hiring or rejection.
- It does **not** score gender, age, religion, nationality, photograph,
  marital status, or disability.
- Match scores are estimates based on text/keyword similarity — missing
  keywords do not always mean missing ability.
- Uploaded resumes are processed from a temporary file and deleted
  immediately after analysis; nothing is stored permanently unless you add
  that feature explicitly.

## Testing

See `tests/test_cases.csv` for the evaluation template. Run the sample
resumes in `sample_resumes/` through the app and fill in the "Actual Top
Role" and "Comments" columns to complete Module 11 (Testing and Evaluation).

## Viva Prep

See the project brief's suggested viva questions (TF-IDF, cosine similarity,
why keyword matching can miss relevant skills, when to use Sentence
Transformers, why protected attributes are excluded, limitations, etc.) —
this README's "How Matching Works" and "Responsible AI Notes" sections cover
the reasoning behind most of them.
