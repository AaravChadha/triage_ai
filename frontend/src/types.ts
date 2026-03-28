export interface Message {
  role: "user" | "assistant";
  content: string;
}

export interface ChatResponse {
  response: string;
  history: Message[];
  is_emergency: boolean;
  triage_ready: boolean;
  emergency_reasoning?: string | null;
}

export interface TriageResponse {
  severity: string;
  confidence: number;
  reasoning: string;
  key_symptoms: string[];
  estimated_duration: string;
  flags: string[];
  required_tier: number;
  required_capabilities: string[];
}

export interface SummaryResponse {
  chief_complaint: string;
  symptoms: string[];
  duration: string;
  pain_level: number;
  relevant_history: string;
  severity: string;
  recommended_care: string;
  ai_notes: string;
}

export interface NotifyResponse {
  success: boolean;
  message: string;
}
