# ResumeIQ AI 🧠

ResumeIQ AI is a full-stack AI-powered resume analysis platform designed to evaluate resumes, detect skill gaps, optimize ATS compatibility, and generate intelligent resume improvement suggestions using Large Language Models (LLMs).

The platform combines FastAPI, Groq-powered LLM inference, PDF parsing, and an interactive analytics dashboard to deliver real-time resume intelligence.

---

## 🚀 Features

### 📄 Resume Analysis
- Upload PDF resumes
- Automatic resume text extraction
- AI-powered career domain detection
- Resume readiness scoring
- Weak area identification
- Missing keyword detection
- ATS optimization suggestions

### 🤖 AI Enhancements
- LLM-generated improved resume bullet points
- Smart keyword recommendations
- Context-aware resume evaluation
- Structured JSON analysis responses

### 📊 Interactive Dashboard
- Resume analytics visualization
- Readiness score breakdown
- Dynamic progress indicators
- Recommended jobs and internships
- Responsive modern UI design

---

## 🛠️ Tech Stack

### Backend
- Python
- FastAPI
- Groq API
- Llama 3.3 70B Versatile
- PyMuPDF (fitz)
- JSON Processing

### Frontend
- HTML5
- CSS3
- JavaScript
- Fetch API

### Other Tools
- dotenv
- CORS Middleware

---

## ⚙️ System Architecture

1. User uploads a PDF resume
2. Backend extracts text using PyMuPDF
3. Resume content is sent to the Groq LLM
4. AI analyzes:
   - Career domain
   - Resume quality
   - Missing skills
   - Weak sections
5. Results are returned as JSON
6. Frontend dashboard visualizes analytics

---

## 📊 AI Analysis Output

The system generates:

- Resume readiness score
- Career domain prediction
- Missing keyword analysis
- Weak area detection
- AI-enhanced resume bullet points
- Recommended jobs and internships

Example:

```json
{
  "domain": "Software Engineering",
  "readiness_score": 86,
  "weak_areas": ["Projects", "Achievements"],
  "missing_keywords": ["Docker", "AWS", "CI/CD"],
  "improved_bullets": [
    {
      "original": "Worked on backend development",
      "improved": "Developed scalable backend APIs improving system efficiency by 35%."
    }
  ]
}
```

---

## ▶️ Installation

### Clone repository

```bash
git clone <repository-url>
cd ResumeIQ-AI
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure environment variables

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key_here
```

---

## ▶️ Run Backend

```bash
uvicorn main:app --reload
```

Backend runs at:

```text
http://127.0.0.1:8000
```

---

## ▶️ Run Frontend

Open:

```text
index.html
```

in your browser.

---

## 📁 API Endpoint

### Analyze Resume

```http
POST /analyze
```

Accepts:
- PDF resume upload

Returns:
- AI-generated resume analysis JSON

---

## 📈 Dashboard Features

- Readiness score visualization
- Keyword analysis pills
- Weak area indicators
- Resume improvement suggestions
- Job recommendation cards
- Responsive dashboard layout

---

## 🔐 Security

- API keys stored securely using environment variables
- CORS-enabled backend communication
- Structured exception handling implemented

---

## 📌 Future Improvements

- Multi-resume comparison
- Job-role-specific optimization
- Authentication system
- Resume ranking engine
- AI interview preparation
- Resume PDF export
- Cloud deployment

---

## 👨‍💻 Author

B S

---

Built with ❤️ using FastAPI, Groq LLMs, and intelligent resume analytics.
