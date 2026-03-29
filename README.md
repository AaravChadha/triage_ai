# Triage AI — AI Pre-Arrival Patient Triage and Care Routing System

**HackIndy 2026 — Purdue Indianapolis**

## What it does

Triage AI helps patients determine the right level of care before leaving home. Instead of everyone going to the ER, the system guides them to the appropriate facility — whether that's emergency care, urgent care, primary care, telehealth, or self-care.

A patient describes their symptoms through a chat interface. The AI asks targeted clinical follow-up questions, detects emergencies in real-time, classifies the severity of the condition, recommends nearby facilities sorted by wait time and capability, and generates a structured pre-arrival patient summary that can be sent to the receiving facility before the patient arrives.

### Key Features

- **AI Triage Conversation** — clinical follow-up questions adapted to the type of injury or illness (pain, injury, illness, mental health)
- **Emergency Detection** — two-layer system: backend keyword matching + AI context analysis. Detects emergencies like cardiac events, stroke, and severe bleeding. Includes "Why?" reasoning so patients can make informed decisions.
- **Atypical Symptom Awareness** — catches commonly missed patterns: women presenting heart attacks with abdominal pain, elderly confusion as infection, diabetic painless cardiac events, young adult stroke dismissed as migraine, falls masking underlying conditions
- **6-Tier Severity Classification** — Call 911, ER, Urgent Care, Primary Care, Telehealth, Self-Care. Conservative by design (when in doubt, recommends higher tier)
- **Facility Finder** — shows nearby facilities filtered by required capabilities and tier, sorted by wait time. Enforces a hard care level floor (never sends a serious case to a lower tier just because wait time is shorter)
- **Pre-Arrival Patient Summary** — clinical-style handoff document with chief complaint, symptoms, severity, recommended care, and AI assessment. Uses preliminary language ("consistent with", "suspected") — never diagnoses.
- **Send to Facility** — patient selects a facility and sends the summary before arriving, so staff can prepare

## Team

- **Team Lead** — Aarav Chadha | Project planning, backend, AI prompt engineering, triage logic, UI polish
- **Frontend Lead** — Neil | Frontend, facility service, UI components

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React, Vite, Tailwind CSS, TypeScript |
| Backend | Python, FastAPI, Uvicorn |
| AI | Groq API, llama-3.3-70b-versatile |
| Facility Data | Mock data (hardcoded facilities near Purdue Indianapolis campus) |
| Other | Pydantic, python-dotenv, httpx, lucide-react |

## What was built during the event

Everything in this repository was built from scratch during HackIndy 2026 (March 28-30). No pre-existing code was used. The project started with an empty directory and a planning document.

**Built during the hackathon:**
- Full FastAPI backend with 5 endpoints (`/chat`, `/triage`, `/facilities`, `/summary`, `/notify`)
- AI prompt engineering for clinical triage conversation, severity classification, and patient summary generation
- Two-layer emergency detection system (keyword + AI context analysis)
- Atypical symptom awareness rules (women cardiac, elderly confusion, diabetic cardiac, young stroke, elderly falls)
- Backend validation that auto-escalates triage tier if AI recommends a tier too low for required capabilities
- React frontend with chat interface, emergency alert, triage result card, facility list, and patient summary
- Mock facility data for Indianapolis-area hospitals, urgent care centers, and telehealth providers

## AI Usage Disclosure

This project uses AI in two ways:

1. **Groq API (llama-3.3-70b-versatile)** — powers the in-app triage system. The AI conducts the symptom conversation, classifies severity, and generates patient summaries. All prompts were written by the team during the hackathon.

2. **Claude Code (Anthropic)** — used as a development assistant during the hackathon for planning, writing code, debugging, and testing. Claude Code helped scaffold the project, write backend endpoints, design AI prompts, and run integration tests.

Both tools are credited here as required by HackIndy rules. The project concept, architecture decisions, clinical logic, and prompt design are original work by the team.

## Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 18+
- A free Groq API key from [groq.com](https://groq.com)

### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp ../.env.example .env
# Edit .env and add your GROQ_API_KEY
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173 in your browser.

## License

Built for HackIndy 2026. Not intended for real medical use.
