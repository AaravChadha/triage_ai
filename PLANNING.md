# AI Pre-Arrival Patient Triage and Care Routing System
### HackIndy — Purdue Indianapolis | 2-Day Hackathon

---

## Problem

Hospitals, especially emergency departments, are overwhelmed because patients arrive at the wrong level of care. Most triage occurs only after a patient arrives. There is no widely available system that helps patients determine the correct level of care before leaving home.

---

## Solution

An AI-powered pre-arrival triage system that:
1. Collects symptom information via a conversational interface
2. Analyzes symptoms using Claude AI
3. Classifies severity and recommends appropriate care level
4. Identifies nearby medical facilities
5. Generates a structured patient summary for the receiving facility

---

## Tech Stack

| Layer | Choice | Reason |
|---|---|---|
| Frontend | React + Vite + Tailwind CSS | Fast setup, chat UI fits well |
| Backend | Python + FastAPI | Best AI library ecosystem, async support |
| AI | Groq API (`llama-3.3-70b-versatile`) | Free, no credit card, fast inference, OpenAI-compatible |
| Maps/Facilities | Google Places API | Best facility data + distance calculation |
| DB | None (in-memory sessions) | Saves setup time for hackathon |
| Deployment | Vercel (frontend) + Railway (backend) | Zero-config hackathon deploys |

---

## System Architecture

```
Patient (Browser)
      │
      ▼
React Chat UI
      │
      ▼
FastAPI Backend
      ├── /chat          → Groq API (conversation + follow-ups)
      ├── /triage        → Groq API (severity classification)
      ├── /facilities    → Google Places API (nearby care)
      ├── /summary       → Groq API (structured patient summary)
      └── /notify        → Mock hospital endpoint
```

---

## Project Structure

```
triage-ai/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatWindow.tsx       # Main chat UI
│   │   │   ├── MessageBubble.tsx    # Individual message
│   │   │   ├── TriageResult.tsx     # Severity + recommendation card
│   │   │   ├── FacilityList.tsx     # Nearby facilities with map
│   │   │   ├── EmergencyAlert.tsx   # Full-screen emergency banner
│   │   │   └── PatientSummary.tsx   # Generated summary card
│   │   ├── hooks/
│   │   │   └── useChat.ts           # Chat state + API calls
│   │   └── App.tsx
│   └── package.json
│
├── backend/
│   ├── main.py                      # FastAPI app + routes
│   ├── services/
│   │   ├── triage_engine.py         # Groq integration + prompts
│   │   ├── facility_service.py      # Google Places integration
│   │   ├── summary_generator.py     # Patient summary generation
│   │   └── emergency_detector.py    # Real-time emergency keyword check
│   ├── models/
│   │   ├── schemas.py               # Pydantic models
│   │   └── triage_levels.py         # Enum: ER / Urgent / Primary / Telehealth / Self
│   ├── prompts/
│   │   ├── conversation.py          # System prompt for follow-up questions
│   │   ├── triage.py                # System prompt for severity classification
│   │   └── summary.py               # System prompt for patient summary
│   └── requirements.txt
│
└── PLANNING.md
```

---

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/chat` | Send message, get AI response + follow-up |
| POST | `/triage` | Finalize triage from full conversation |
| POST | `/facilities` | Get nearby facilities by level + location |
| POST | `/summary` | Generate structured patient summary |
| POST | `/notify` | Send summary to mock hospital endpoint |

---

## Conversation Flow (State Machine)

```
STATE 1: INTAKE
  → "Describe your symptoms"
  → Claude asks up to 4 follow-up questions:
     - Duration
     - Pain level (1–10)
     - Relevant history (diabetes, heart conditions, etc.)
     - Current medications

STATE 2: EMERGENCY CHECK (runs after every user message)
  → Pattern match + Claude check for red flags
  → Red flags: chest pain + SOB, stroke symptoms, severe bleeding,
    unresponsiveness, anaphylaxis
  → If detected → EXIT to EMERGENCY ALERT immediately

STATE 3: TRIAGE ANALYSIS
  → Claude receives full conversation context
  → Returns structured JSON:
    {
      "severity": "urgent_care",
      "confidence": 0.87,
      "reasoning": "...",
      "key_symptoms": [...],
      "estimated_duration": "...",
      "flags": [...]
    }

STATE 4: FACILITY RECOMMENDATION
  → User shares location (browser geolocation)
  → Google Places query filtered by severity level
  → Returns top 3 nearby facilities with distance + hours

STATE 5: SUMMARY GENERATION
  → Claude generates structured patient summary
  → Displayed on screen, optionally sent to mock hospital endpoint
```

---

## Triage Levels

| Level | Label | When |
|---|---|---|
| 0 | **Call 911** | Life-threatening emergency detected |
| 1 | **Emergency Room** | High severity, needs immediate evaluation |
| 2 | **Urgent Care** | Needs same-day care, not life-threatening |
| 3 | **Primary Care** | Can wait 1–2 days for appointment |
| 4 | **Telehealth** | Minor symptoms, remote consult sufficient |
| 5 | **Self-Care** | Rest/OTC meds likely sufficient |

---

## Key Design Decisions

1. **Emergency detection runs client-side too** — don't wait for an API round trip. Simple keyword matching on the frontend as a first layer.
2. **Groq does one structured output call for triage** — after conversation ends, one final call with the full transcript returns the JSON triage object. Keeps it deterministic. Use `llama-3.3-70b-versatile` as primary, `mixtral-8x7b-32768` as fallback for longer context.
3. **No database** — session data lives in-memory on the backend. Saves setup time for the hackathon.
4. **No real patient data stored** — ephemeral sessions only. Design defensively even without HIPAA compliance.
5. **Facility search enforces capability matching before wait time** — the AI triage output includes `required_tier` and `required_capabilities`. The facility service first filters to only facilities that can actually treat the condition (e.g., a patient needing stitches cannot be sent to Telehealth). Within that eligible set, Levels 1–2 are locked to Tier 1–2 only. Levels 3–5 are flexible. Wait time is used last, as the final tiebreaker among eligible facilities.

---

---

## Phases, Tasks, and Subtasks

### Phase 0 — Project Setup `Friday 5–8pm` (~1 hr)
> Goal: Everyone can run the project locally before writing any real code.

- [x] **0.1 Repo & Structure**
  - [x] 0.1.1 Initialize git repo
  - [x] 0.1.2 Create `/frontend` and `/backend` folders
  - [x] 0.1.3 Add `.gitignore` (node_modules, __pycache__, .env)
  - [x] 0.1.4 Add `.env.example` with required keys (`GROQ_API_KEY`, `GOOGLE_PLACES_API_KEY`)

- [x] **0.2 Backend Bootstrap**
  - [x] 0.2.1 Create Python virtual environment
  - [x] 0.2.2 Install dependencies: `fastapi`, `uvicorn`, `groq`, `python-dotenv`, `httpx`
  - [x] 0.2.3 Create `requirements.txt`
  - [x] 0.2.4 Create `main.py` with a health check route (`GET /health`)
  - [x] 0.2.5 Confirm server runs with `uvicorn main:app --reload`

- [x] **0.3 Frontend Bootstrap**
  - [x] 0.3.1 Scaffold React app with Vite (`npm create vite@latest`)
  - [x] 0.3.2 Install Tailwind CSS
  - [x] 0.3.3 Delete boilerplate, create empty `App.tsx`
  - [x] 0.3.4 Confirm dev server runs with `npm run dev`

- [x] **0.4 API Keys**
  - [x] 0.4.1 Sign up at groq.com and get free API key
  - [x] 0.4.2 ~~Sign up at Google Cloud Console and enable Places API~~ — skipped, will use mock fallback
  - [x] 0.4.3 Add keys to `.env`

---

### Phase 1 — Core AI Backend `Friday 8pm → Saturday 12pm` (~3–4 hrs, includes overnight)
> Goal: The AI can receive symptoms, ask follow-up questions, and return a triage result.
> **Build order:** 1.1 → 1.3 → 1.2 → 1.4 → 1.6 → 1.5 → 1.7 (share schemas after 1.3 to unblock teammates)

- [x] **1.1 Groq Client Setup** ← start here
  - [x] 1.1.1 Create `services/triage_engine.py`
  - [x] 1.1.2 Initialize Groq client from env variable
  - [x] 1.1.3 Write a basic test call to confirm connection

- [x] **1.3 Pydantic Models** ← do second, share with teammates immediately after
  - [x] 1.3.1 Create `models/schemas.py` — request/response models for each endpoint
  - [x] 1.3.2 Create `models/triage_levels.py` — enum for 6 triage levels with required facility capabilities per tier:
    - Tier 1 (ER): trauma care, imaging, surgery, ICU
    - Tier 2 (Urgent Care): X-ray, stitches, IV fluids, basic labs
    - Tier 3 (Primary Care): general consultation, prescriptions, referrals
    - Tier 4 (Telehealth): video consult, e-prescriptions only
    - Tier 5 (Self-Care): no facility needed

- [x] **1.2 Conversation Prompts** ← do third
  - [x] 1.2.1 Create `prompts/conversation.py` — system prompt for follow-up questioning (clinical tone, no explanations, 3-5 questions max, EMERGENCY_DETECTED / TRIAGE_READY signals)
  - [x] 1.2.2 Create `prompts/triage.py` — system prompt for severity classification (Tier 0 shows 911 + nearest ER, returns JSON with tier, capabilities, confidence)
  - [x] 1.2.3 Create `prompts/summary.py` — system prompt for pre-arrival clinical summary sent to facility, structured JSON, preliminary AI assessment language

- [x] **1.4 Triage → Tier Mapping** ← do fourth
  - [x] 1.4.1 AI triage output must include `required_tier` and `required_capabilities` (e.g., `["imaging", "IV fluids"]`) — built into triage prompt (1.2.2) and schema (1.3.1)
  - 1.4.2 and 1.4.3 moved to Phase 3.5 (needs facility service first)

- [x] **1.6 Emergency Detector** ← do fifth (needed before /chat)
  - [x] 1.6.1 Create `services/emergency_detector.py`
  - [x] 1.6.2 Define keyword/phrase list for red flag symptoms
  - 1.6.3 and 1.6.4 moved to 1.5 (wired into /chat endpoint)

- [x] **1.5 `/chat` Endpoint** ← do sixth, unblocks Teammate 1
  - [x] 1.5.1 Accept message + conversation history
  - [x] 1.5.2 Run emergency detector first — if triggered, return immediately with `is_emergency: true` without calling Groq (1.6.3 + 1.6.4)
  - [x] 1.5.3 Pass to Groq with conversation system prompt
  - [x] 1.5.4 Return AI response + updated history — done in 1.5.3
  - [x] 1.5.5 Test with Postman or curl

- [x] **1.7 `/triage` Endpoint** ← do last, unblocks Teammates 1 + 2
  - [x] 1.7.1 Accept full conversation history
  - [x] 1.7.2 Call Groq with triage classification prompt
  - [x] 1.7.3 Parse and validate returned JSON
  - [x] 1.7.4 Return structured triage result (severity, confidence, reasoning, key symptoms)

- [x] **1.8 Phase 1 Integration Test**
  - [x] 1.8.1 Test `/chat` end-to-end: normal message → AI follow-up → emergency message → `is_emergency: true`
  - [x] 1.8.2 Test `/triage` end-to-end: send full conversation → get valid JSON with correct tier and capabilities
  - [x] 1.8.3 Verify emergency detector doesn't false-positive on mild symptoms (e.g. "slight cough", "runny nose")
  - [x] 1.8.4 Verify TRIAGE_READY signal fires after enough questions

---

### Phase 2 — Frontend Chat Interface `Saturday 12pm → 5pm` (~2–3 hrs)
> Goal: User can have a full conversation in the browser and see a triage result.

- [x] **2.1 Chat UI Layout**
  - [x] 2.1.1 Build `ChatWindow.tsx` — scrollable message area + input bar
  - [x] 2.1.2 Build `MessageBubble.tsx` — distinct styles for user vs AI messages
  - [x] 2.1.3 Wire input to send message on Enter or button click

- [x] **2.2 Connect to Backend**
  - [x] 2.2.1 Create `hooks/useChat.ts` — manages message state and API calls
  - [x] 2.2.2 Call `POST /chat` on each user message
  - [x] 2.2.3 Append AI response to message list
  - [x] 2.2.4 Handle loading state (show typing indicator)

- [x] **2.3 Emergency Alert**
  - [x] 2.3.1 Build `EmergencyAlert.tsx` — full-screen red overlay
  - [x] 2.3.2 Show bold "Call 911 immediately" message with emergency icon + "Continue" button if the user believes it's not an emergency + "Why?" button that shows `emergency_reasoning` from ChatResponse
  - [x] 2.3.3 Trigger when backend returns `is_emergency: true`
  - [x] 2.3.4 Add client-side keyword check as a first-pass layer (no API wait) — reuse patterns from `services/emergency_detector.py`

- [x] **2.4 Triage Trigger**
  - [x] 2.4.1 Show "Analyze My Symptoms" button when backend returns `triage_ready: true` in ChatResponse
  - [x] 2.4.2 Call `POST /triage` with full conversation history
  - [x] 2.4.3 Show loading state while waiting

- [x] **2.5 Triage Result Card**
  - [x] 2.5.1 Build `TriageResult.tsx`
  - [x] 2.5.2 Display severity level with color coding (red = ER, orange = urgent, green = self-care)
  - [x] 2.5.3 Show reasoning and key symptoms
  - [x] 2.5.4 Show confidence level

---

### Phase 3 — Facility Finder `Saturday 5pm → Sunday 10am` (~4–5 hrs, includes overnight)
> Goal: After triage, user sees nearby facilities appropriate for their care level. Using mock facility data near Purdue Indianapolis campus (can swap in Google Places API later if free credits available).

- [ ] **3.1 Backend Facility Service**
  - [ ] 3.1.1 Create `services/facility_service.py`
  - [ ] 3.1.2 ~~Implement Google Places API~~ — using mock data for now (can swap in Google Places API if MLH provides free Google Cloud credits)
  - [ ] 3.1.3 Map triage level → facility type (e.g., Level 2 → "urgent care")
  - [ ] 3.1.4 Filter facilities by `required_capabilities` from triage output — a facility must be capable of treating the condition before it is considered (e.g., don't send a patient needing stitches to a telehealth provider)
  - [ ] 3.1.5 Return top 3 results with name, address, distance, open status — from capable facilities only
  - [ ] 3.1.6 Attach mock wait time to each facility based on care level tier:
    - Emergency Room: random 45–120 min → display as `~X min wait`
    - Urgent Care: random 15–45 min → display as `~X min wait`
    - Primary Care: no wait time → display as `Next appt: tomorrow`
    - Telehealth: random 0–5 min → display as `Available now` or `~X min wait`
  - [ ] 3.1.7 Enforce hard care level floor based on severity:
    - Levels 1–2 (Emergency / High Urgency): only show Tier 1 (ER) or Tier 2 (Urgent Care) — never route to lower tiers regardless of wait time
    - Levels 3–5 (Primary / Telehealth / Self-Care): show recommended tier but also surface lower tiers as alternatives if wait time is significantly shorter
  - [ ] 3.1.8 Sort returned facilities by wait time ascending (shortest wait first) — within the allowed tier floor only

- [ ] **3.2 `/facilities` Endpoint**
  - [ ] 3.2.1 Accept triage level + lat/lng coordinates
  - [ ] 3.2.2 Call facility service and return results (including wait time field)
  - [ ] 3.2.3 Hardcoded facility list defined as a static dict in `facility_service.py`, keyed by triage level — mock facilities should be real or realistic locations near Purdue Indianapolis campus (demo will be presented there)

- [ ] **3.3 Frontend Location + Facility List**
  - [ ] 3.3.1 Request browser geolocation on triage completion
  - [ ] 3.3.2 Call `POST /facilities` with coordinates + severity
  - [ ] 3.3.3 Build `FacilityList.tsx` — show each facility as a card with name, address, distance, and wait time
  - [ ] 3.3.4 Highlight the top result as "Recommended" (closest + shortest wait)
  - [ ] 3.3.5 Link each facility to Google Maps directions

---

### Phase 3.5 — Triage ↔ Facility Integration (Aarav) `after Phase 3`
> Goal: Wire up the triage output to the facility service so filtering and validation actually work end-to-end.

- [ ] **1.4 Triage → Tier Mapping (deferred from Phase 1)**
  - [ ] 1.4.2 Pass `required_tier` and `required_capabilities` from triage output to facility service filter
  - [ ] 1.4.3 Add backend validation that the AI never recommends a tier incapable of treating the identified condition (e.g., a laceration needing stitches cannot be sent to Tier 4 Telehealth)

---

### Phase 4 — Patient Summary `Sunday 10am → 1pm` (~1–2 hrs)
> Goal: Generate and display a structured patient summary that could be sent to a facility. This is the demo "wow" moment — prioritize this over facility polish if time is short.

- [x] **4.1 `/summary` Endpoint**
  - [x] 4.1.1 Accept full conversation + triage result
  - [x] 4.1.2 Call Groq with summary prompt
  - [x] 4.1.3 Return structured summary: chief complaint, symptom list, duration, severity, AI notes

- [x] **4.2 Summary UI**
  - [x] 4.2.1 Build `PatientSummary.tsx` — clean formatted card
  - [x] 4.2.2 Show all fields clearly in this order: chief complaint → symptoms → duration → pain level → relevant history → severity classification → recommended care → AI notes
  - [x] 4.2.3 Add "Send to Facility" button that calls `POST /notify` (mock)

- [x] **4.3 Mock Hospital Notification**
  - [x] 4.3.1 Create `POST /notify` endpoint
  - [x] 4.3.2 Accept summary payload, log it, return success
  - [ ] 4.3.3 Show confirmation toast on frontend: "Summary sent to [Facility Name]" — Neil

---

### Phase 5 — Polish and Demo Prep `Sunday 1pm → 4pm` (~1–2 hrs)
> Goal: The happy path is flawless and the app looks good in front of judges. The four things judges will evaluate: (1) Groq conversation flow with follow-ups, (2) emergency detection with full-screen alert, (3) triage classification with clear severity output, (4) patient summary generation.

- [ ] **5.1 UI Polish**
  - [ ] 5.1.1 Consistent color scheme and typography
    > **Ask before building:** Confirm the color palette — suggested: red = ER, orange = urgent care, yellow = primary care, blue = telehealth, green = self-care. Any brand preferences?
  - [ ] 5.1.2 App header with name and tagline
  - [ ] 5.1.3 Responsive layout (works on laptop screen during demo)
  - [ ] 5.1.4 Smooth transitions between chat, triage result, and facility list

- [ ] **5.2 Error Handling**
  - [ ] 5.2.1 Show friendly message if Groq API call fails — backend already returns 503 with emergency instructions, frontend needs to display it
  - [ ] 5.2.2 Show friendly message if location access is denied
  - [ ] 5.2.3 Prevent double-submitting messages

---

## Phase 6 — Submission Checklist `Sunday 3–4pm`
> Goal: Meet all HackIndy submission requirements before deadline.

- [ ] **6.1 README.md**
  - [ ] 6.1.1 Write project description — what it does and why it matters
  - [ ] 6.1.2 List all technologies/frameworks used (React, Vite, Tailwind, FastAPI, Groq, llama-3.3-70b-versatile)
  - [ ] 6.1.3 Clear explanation of what was built during the event (not before)
  - [ ] 6.1.4 AI usage disclosure — list all AI tools used (Claude Code for development assistance, Groq API for triage AI). Be specific about what each tool did. Do NOT misrepresent AI-generated code as hand-written.
  - [ ] 6.1.5 Credit all libraries, APIs, and tools used
  - [ ] 6.1.6 Setup instructions: clone → create `backend/.env` with your own `GROQ_API_KEY` (free at groq.com) → install → run

- [ ] **6.2 Repo Cleanup**
  - [ ] 6.2.1 Confirm `.env` is NOT committed (check with `git log --all -- '*.env'`)
  - [ ] 6.2.2 Confirm `.env.example` exists with placeholder keys
  - [ ] 6.2.3 Remove any debug/test code
  - [ ] 6.2.4 Confirm repo is public on GitHub

- [ ] **6.3 Final Checks**
  - [ ] 6.3.1 Submit GitHub repo link to HackIndy submission portal
  - [ ] 6.3.2 Verify the app runs from a fresh clone (after adding your own `.env` with Groq key)
  - [ ] 6.3.3 Double-check README covers all submission requirements: description, tech stack, what was built, AI disclosure

---

### Phase 7 — Demo Rehearsal `Sunday 4pm`
> Goal: The happy path is flawless in front of judges. Do this AFTER submission is ready.

- [ ] **7.1 Demo Rehearsal**
  - [ ] 7.1.1 Run through Scenario 1 (emergency) — confirm alert fires correctly
  - [ ] 7.1.2 Run through Scenario 2 (urgent care) — confirm full flow works end to end
  - [ ] 7.1.3 Time the demo — target under 3 minutes
  - [ ] 7.1.4 Prepare a 1-sentence answer for "what happens with patient data?"

---

## Demo Script for Judges

**Scenario 1 — Emergency (shows the safety feature):**
> "It's 2am. Someone wakes up with chest tightness and mild shortness of breath."
- User types symptoms → AI asks follow-ups → emergency alert fires → red full-screen banner, call 911

**Scenario 2 — Urgent Care (shows the full flow):**
> "Stomach pain for 2 days, no fever, pain level 5/10."
- AI asks follow-ups → recommends urgent care → shows 3 nearby facilities → generates patient summary

This arc demonstrates every feature in under 3 minutes.

---

## Future Extensions (mention to judges, don't build)
- Hospital wait time data integration
- Insurance network compatibility
- EHR integration
- Predictive ED congestion analytics
- Public health trend detection from aggregated symptoms
