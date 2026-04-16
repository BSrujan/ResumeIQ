import fitz
import json
import os
from groq import Groq
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load env variables
load_dotenv()

app = FastAPI()

# ✅ Restrict CORS (change frontend URL if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ✅ Health check endpoint
@app.get("/health")
def health():
    return {"status": "running"}

# ✅ Resume Analyzer Endpoint
@app.post("/analyze")
async def analyze_resume(file: UploadFile = File(...)):
    try:
        # ✅ File validation
        if file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")

        contents = await file.read()

        # ✅ Extract text from PDF
        pdf = fitz.open(stream=contents, filetype="pdf")
        text = "".join([page.get_text() for page in pdf])
        pdf.close()

        # ✅ Clean + limit text
        text = " ".join(text.split())
        MAX_CHARS = 6000
        text = text[:MAX_CHARS]

        # ✅ Prompt improvement
        prompt = f"""
        You are a expert resume reviewer.

        Analyze the entire resume, not just work experience.

        Return ONLY valid JSON.
         
        Rules:
        - readiness_score must be between 0–100
        - Analyze the FULL resume (not just experience)
        - Every improved bullet MUST be at least 12 words
        - MUST include measurable impact (%, numbers, results)
        - MUST start with a strong action verb (Developed, Built, Led, Optimized, etc.)
        - DO NOT return short or incomplete phrases
        - Return only top 3 most important bullet improvements
        - final_recommendations must be clear, actionable, and based on overall resume analysis
    - each point should target a specific area (skills, projects, formatting, experience, ATS)

        Focus on:
        - Overall resume quality
        - Structure and formatting
        - Skills section
        - Projects section
        - Work experience
        - ATS optimization



        Resume:
        {text}

        Output format:
        {{
            "domain": "",
            "readiness_score": 0,
            "overall_feedback": "brief summary of resume quality",

            "section_analysis": {{
                "summary": "feedback on summary/objective",
                "skills": "feedback on skills section",
                "projects": "feedback on projects",
                "experience": "feedback on work experience",
                "education": "feedback on education",
                "formatting": "ATS and formatting issues"
         }},

        "weak_areas": [],

        "missing_keywords": [],

        "improvement_suggestions": [],

        "final_recommendations": [
            "clear bullet point suggestion 1",
            "clear bullet point suggestion 2",
            "clear bullet point suggestion 3"
        ],
        "improved_bullets": [
            {{
                "original": "",
                "improved": "Rewrite the bullet with strong action verbs, include measurable impact (numbers, %, results), and make it 1 full sentence (minimum 12 words)"
            }}
      ]
}}
"""

        # ✅ LLM call
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        raw = response.choices[0].message.content.strip()

        # ✅ Clean markdown if present
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        raw = raw.strip()

        # ✅ JSON safety handling
        try:
            result = json.loads(raw)
        except json.JSONDecodeError as e:
            return {
                "error": "Invalid JSON from model",
                "details": str(e),
                "raw_output": raw
            }

        # ✅ Simple keyword logic (extra intelligence)
        common_keywords = ["python", "machine learning", "sql", "api", "data analysis"]

        found = [kw for kw in common_keywords if kw.lower() in text.lower()]
        missing = list(set(common_keywords) - set(found))

        result["detected_keywords"] = found
        result["missing_keywords_backend"] = missing

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))