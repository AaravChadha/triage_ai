export interface Message {
  role: "user" | "assistant";
  content: string;
}

export interface ChatResponse {
  response: string;
  history: Message[];
  is_emergency: boolean;
  triage_ready: boolean;
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
