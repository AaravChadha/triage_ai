from pydantic import BaseModel


# --- Shared ---

class Message(BaseModel):
    role: str   # "user" or "assistant"
    content: str


# --- /chat ---

class ChatRequest(BaseModel):
    message: str
    history: list[Message] = []

class ChatResponse(BaseModel):
    response: str
    history: list[Message]
    is_emergency: bool
    triage_ready: bool = False


# --- /triage ---

class TriageRequest(BaseModel):
    history: list[Message]

class TriageResponse(BaseModel):
    severity: str
    confidence: float
    reasoning: str
    key_symptoms: list[str]
    estimated_duration: str
    flags: list[str]
    required_tier: int
    required_capabilities: list[str]


# --- /facilities ---

class FacilitiesRequest(BaseModel):
    triage_level: int
    lat: float
    lng: float

class Facility(BaseModel):
    name: str
    address: str
    distance_miles: float
    is_open: bool
    wait_time: str
    maps_url: str
    is_recommended: bool

class FacilitiesResponse(BaseModel):
    facilities: list[Facility]


# --- /summary ---

class SummaryRequest(BaseModel):
    history: list[Message]
    triage_result: TriageResponse

class SummaryResponse(BaseModel):
    chief_complaint: str
    symptoms: list[str]
    duration: str
    pain_level: int
    relevant_history: str
    severity: str
    recommended_care: str
    ai_notes: str


# --- /notify ---

class NotifyRequest(BaseModel):
    summary: SummaryResponse
    facility_name: str

class NotifyResponse(BaseModel):
    success: bool
    message: str
