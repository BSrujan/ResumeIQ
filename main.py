import fitz
import json
from groq import Groq
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.post("/analyze")
async def analyze_resume(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        pdf = fitz.open(stream=contents, filetype="pdf")
        text = ""
        for page in pdf:
            text += page.get_text()

        prompt = f"""
        You are an expert resume analyst. Analyze the resume text below and return ONLY a JSON object.
        No markdown, no backticks, no extra text before or after. Just raw JSON.

        Resume text:
        {text}

        Return exactly this JSON structure:
        {{
            "domain": "the main career domain of this person",
            "readiness_score": 75,
            "weak_areas": ["area1", "area2", "area3"],
            "missing_keywords": ["keyword1", "keyword2", "keyword3"],
            "improved_bullets": [
                {{
                    "original": "original bullet point from resume",
                    "improved": "rewritten version with impact and numbers"
                }}
            ]
        }}
        """

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        raw = response.choices[0].message.content.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        raw = raw.strip()

        result = json.loads(raw)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))