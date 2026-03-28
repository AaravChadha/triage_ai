from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.schemas import ChatRequest, ChatResponse, Message
from services.emergency_detector import check_emergency

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
