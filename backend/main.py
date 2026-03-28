import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models.schemas import ChatRequest, ChatResponse, TriageRequest, TriageResponse, SummaryRequest, SummaryResponse, Message
from services.emergency_detector import check_emergency
from services.triage_engine import client, MODEL
from prompts.conversation import CONVERSATION_SYSTEM_PROMPT
from prompts.triage import TRIAGE_SYSTEM_PROMPT

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


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    history = req.history + [Message(role="user", content=req.message)]

    if check_emergency(req.message):
        history.append(Message(role="assistant", content="EMERGENCY DETECTED — Call 911 immediately. If you cannot transport yourself, stay where you are and wait for paramedics. If you believe this is not an emergency, you can continue describing your symptoms."))
        return ChatResponse(
            response=history[-1].content,
            history=history,
            is_emergency=True,
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
        emergency_msg = "EMERGENCY DETECTED — Call 911 immediately. If you cannot transport yourself, stay where you are and wait for paramedics. If you believe this is not an emergency, you can continue describing your symptoms."
        history.append(Message(role="assistant", content=emergency_msg))
        return ChatResponse(
            response=emergency_msg,
            history=history,
            is_emergency=True,
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


@app.post("/summary", response_model=SummaryResponse)
async def summary(req: SummaryRequest):
    pass
