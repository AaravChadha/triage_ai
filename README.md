# Triage AI — AI Pre-Arrival Patient Triage and Care Routing System

**HackIndy 2026 — Purdue Indianapolis**

## What it does

Triage AI helps patients determine the right level of care before leaving home. Instead of everyone going to the ER, the system guides them to the appropriate facility — whether that's emergency care, urgent care, primary care, telehealth, or self-care.

A patient describes their symptoms through a chat interface. The AI asks targeted clinical follow-up questions, detects emergencies in real-time, classifies the severity of the condition, recommends nearby facilities sorted by wait time and capability, and generates a structured pre-arrival patient summary that can be sent to the receiving facility before the patient arrives.

### Key Features

- **AI Triage Conversation** — clinical follow-up questions adapted to the type of injury or illness (pain, injury, illness, mental health)
- **Emergency Detection** — two-layer system: instant keyword matching + AI context analysis. Detects emergencies like cardiac events, stroke, and severe bleeding. Includes "Why?" reasoning so patients can make informed decisions.
- **Atypical Symptom Awareness** — catches commonly missed patterns: women presenting heart attacks with abdominal pain, elderly confusion as infection, diabetic painless cardiac events, young adult stroke dismissed as migraine, falls masking underlying conditions
- **6-Tier Severity Classification** — Call 911, ER, Urgent Care, Primary Care, Telehealth, Self-Care. Conservative by design (when in doubt, recommends higher tier)
- **Facility Finder** — shows nearby facilities filtered by required capabilities and tier, sorted by wait time. Enforces a hard care level floor (never sends a serious case to a lower tier just because wait time is shorter)
- **Pre-Arrival Patient Summary** — clinical-style handoff document with chief complaint, symptoms, severity, recommended care, and AI assessment. Uses preliminary language ("consistent with", "suspected") — never diagnoses.
- **Send to Facility** — patient selects a facility and sends the summary before arriving, so staff can prepare
