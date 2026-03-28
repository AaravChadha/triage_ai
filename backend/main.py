import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models.schemas import ChatRequest, ChatResponse, TriageRequest, TriageResponse, Message
from services.emergency_detector import check_emergency
from services.triage_engine import client
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
        history.append(Message(role="assistant", content="EMERGENCY DETECTED — Call 911 immediately. If you cannot transport yourself, stay where you are and wait for paramedics."))
        return ChatResponse(
            response=history[-1].content,
            history=history,
            is_emergency=True,
        )

    messages = [{"role": "system", "content": CONVERSATION_SYSTEM_PROMPT}]
    messages += [{"role": m.role, "content": m.content} for m in history]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
    )

    ai_message = response.choices[0].message.content

    # AI detected emergency from context (prompt tells it to say EMERGENCY_DETECTED)
    if "EMERGENCY_DETECTED" in ai_message:
        emergency_msg = "EMERGENCY DETECTED — Call 911 immediately. If you cannot transport yourself, stay where you are and wait for paramedics."
        history.append(Message(role="assistant", content=emergency_msg))
        return ChatResponse(
            response=emergency_msg,
            history=history,
            is_emergency=True,
        )

    history.append(Message(role="assistant", content=ai_message))

    return ChatResponse(
        response=ai_message,
        history=history,
        is_emergency=False,
    )


@app.post("/triage", response_model=TriageResponse)
async def triage(req: TriageRequest):
    messages = [{"role": "system", "content": TRIAGE_SYSTEM_PROMPT}]
    messages += [{"role": m.role, "content": m.content} for m in req.history]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
    )

    ai_message = response.choices[0].message.content

    # Strip markdown code fences if the AI wraps JSON in ```json ... ```
    cleaned = ai_message.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[1]
        cleaned = cleaned.rsplit("```", 1)[0]

    try:
        data = json.loads(cleaned)
        result = TriageResponse(**data)
    except (json.JSONDecodeError, Exception):
        raise HTTPException(status_code=500, detail="AI returned invalid triage JSON")

    return result
