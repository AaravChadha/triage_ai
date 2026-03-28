import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models.schemas import ChatRequest, ChatResponse, TriageRequest, TriageResponse, SummaryRequest, SummaryResponse, NotifyRequest, NotifyResponse, Message, FacilitiesRequest, FacilitiesResponse
from services.emergency_detector import check_emergency
from services.triage_engine import client, MODEL
from prompts.conversation import CONVERSATION_SYSTEM_PROMPT
from prompts.triage import TRIAGE_SYSTEM_PROMPT
from prompts.summary import SUMMARY_SYSTEM_PROMPT
from services.facility_service import get_nearby_facilities

app = FastAPI(title="Triage AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


def get_emergency_reasoning(history: list[Message]) -> str:
    """Ask Groq to explain why these symptoms are flagged as an emergency."""
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a clinical triage assistant. The patient's symptoms have been flagged as a potential emergency. Explain in 2-3 sentences why these symptoms are concerning and why calling 911 is recommended. Be specific about what the symptoms could indicate. Do not diagnose — use 'could indicate' or 'consistent with' language."},
                *[{"role": m.role, "content": m.content} for m in history],
            ],
        )
        return response.choices[0].message.content or ""
    except Exception:
        return "Your symptoms match patterns associated with serious medical conditions that require immediate evaluation."


EMERGENCY_MSG = "EMERGENCY DETECTED — Call 911 immediately. If you cannot transport yourself, stay where you are and wait for paramedics. If you believe this is not an emergency, you can continue describing your symptoms."


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    history = req.history + [Message(role="user", content=req.message)]

    if check_emergency(req.message):
        reasoning = get_emergency_reasoning(history)
        history.append(Message(role="assistant", content=EMERGENCY_MSG))
        return ChatResponse(
            response=EMERGENCY_MSG,
            history=history,
            is_emergency=True,
            emergency_reasoning=reasoning,
        )

    messages = [{"role": "system", "content": CONVERSATION_SYSTEM_PROMPT}]
    messages += [{"role": m.role, "content": m.content} for m in history]

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
        )
        ai_message = response.choices[0].message.content
    except Exception:
        raise HTTPException(status_code=503, detail="AI service is temporarily unavailable. Please try again. If you are experiencing a medical emergency, call 911 immediately.")

    # AI detected emergency from context (prompt tells it to say EMERGENCY_DETECTED)
    if "EMERGENCY_DETECTED" in ai_message:
        reasoning = get_emergency_reasoning(history)
        history.append(Message(role="assistant", content=EMERGENCY_MSG))
        return ChatResponse(
            response=EMERGENCY_MSG,
            history=history,
            is_emergency=True,
            emergency_reasoning=reasoning,
        )

    # AI has enough info to triage
    if "TRIAGE_READY" in ai_message:
        ready_msg = "I have enough information. Ready to analyze your symptoms."
        history.append(Message(role="assistant", content=ready_msg))
        return ChatResponse(
            response=ready_msg,
            history=history,
            is_emergency=False,
            triage_ready=True,
        )

    history.append(Message(role="assistant", content=ai_message))

    return ChatResponse(
        response=ai_message,
        history=history,
        is_emergency=False,
    )


@app.post("/triage", response_model=TriageResponse)
async def triage(req: TriageRequest):
    # Filter out TRIAGE_READY/EMERGENCY_DETECTED signals from history
    filtered = [m for m in req.history if m.content not in ("TRIAGE_READY", "EMERGENCY_DETECTED")]

    # If last message is from assistant, the user never answered — add a note so the AI knows
    if filtered and filtered[-1].role == "assistant":
        filtered.append(Message(role="user", content="(patient did not respond, proceed with triage based on available information)"))

    messages = [{"role": "system", "content": TRIAGE_SYSTEM_PROMPT}]
    messages += [{"role": m.role, "content": m.content} for m in filtered]

    # Try up to 2 times in case of empty or invalid response
    for attempt in range(2):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
            )
            ai_message = response.choices[0].message.content or ""
        except Exception:
            raise HTTPException(status_code=503, detail="AI service is temporarily unavailable. Please try again. If you are experiencing a medical emergency, call 911 immediately.")

        # Strip markdown code fences if the AI wraps JSON in ```json ... ```
        cleaned = ai_message.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("\n", 1)[1]
            cleaned = cleaned.rsplit("```", 1)[0]
        cleaned = cleaned.strip()

        try:
            data = json.loads(cleaned)
            return TriageResponse(**data)
        except (json.JSONDecodeError, Exception):
            continue

    raise HTTPException(status_code=500, detail="AI returned invalid triage JSON")


@app.post("/facilities", response_model=FacilitiesResponse)
async def get_facilities(req: FacilitiesRequest):
    results = get_nearby_facilities(
        triage_level=req.triage_level,
        lat=req.lat,
        lng=req.lng,
        required_capabilities=req.required_capabilities,
    )
    return FacilitiesResponse(facilities=results)


@app.post("/summary", response_model=SummaryResponse)
async def summary(req: SummaryRequest):
    # Build context: conversation history + triage result
    triage_context = f"TRIAGE RESULT: severity={req.triage_result.severity}, tier={req.triage_result.required_tier}, confidence={req.triage_result.confidence}, key_symptoms={req.triage_result.key_symptoms}, reasoning={req.triage_result.reasoning}"

    messages = [{"role": "system", "content": SUMMARY_SYSTEM_PROMPT}]
    messages += [{"role": m.role, "content": m.content} for m in req.history if m.content not in ("TRIAGE_READY", "I have enough information. Ready to analyze your symptoms.")]
    messages.append({"role": "user", "content": triage_context})

    for attempt in range(2):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
            )
            ai_message = response.choices[0].message.content or ""
        except Exception:
            raise HTTPException(status_code=503, detail="AI service is temporarily unavailable. Please try again.")

        cleaned = ai_message.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("\n", 1)[1]
            cleaned = cleaned.rsplit("```", 1)[0]
        cleaned = cleaned.strip()

        try:
            data = json.loads(cleaned)
            return SummaryResponse(**data)
        except (json.JSONDecodeError, Exception):
            continue

    raise HTTPException(status_code=500, detail="AI returned invalid summary JSON")


@app.post("/notify", response_model=NotifyResponse)
async def notify(req: NotifyRequest):
    print(f"[NOTIFY] Summary sent to {req.facility_name}")
    print(f"  Chief complaint: {req.summary.chief_complaint}")
    print(f"  Severity: {req.summary.severity}")
    return NotifyResponse(
        success=True,
        message=f"Summary sent to {req.facility_name}",
    )
