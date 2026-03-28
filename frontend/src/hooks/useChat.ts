import { useState, useCallback } from 'react';
import { Message, ChatResponse, TriageResponse } from '../types';

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isEmergency, setIsEmergency] = useState(false);
  const [triageReady, setTriageReady] = useState(false);
  const [triageResult, setTriageResult] = useState<TriageResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const API_BASE_URL = 'http://localhost:8000'; 

  const checkEmergencyKeywords = (text: string) => {
    const list = ['chest pain', 'hurt to breathe', 'can\'t breathe', 'stroke', 'bleeding out', 'gunshot', 'suicide'];
    const lower = text.toLowerCase();
    return list.some(keyword => lower.includes(keyword));
  };

  const sendMessage = useCallback(async (content: string) => {
    const userMessage: Message = { role: 'user', content };
    setMessages((prev: Message[]) => [...prev, userMessage]);
    setError(null);

    if (checkEmergencyKeywords(content)) {
      setIsEmergency(true);
      return; 
    }

    setIsLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: content,
          history: messages 
        })
      });

      if (!response.ok) {
        throw new Error('Failed to send message');
      }

      const data: ChatResponse = await response.json();
      
      if (data.is_emergency) {
         setIsEmergency(true);
      }
      
      setMessages(data.history);
      setTriageReady(data.triage_ready);

    } catch (err: any) {
      setError(err.message || 'An error occurred');
      console.error('Chat error:', err);
    } finally {
      setIsLoading(false);
    }
  }, [messages]);

  const analyzeSymptoms = useCallback(async () => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_BASE_URL}/triage`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          history: messages
        })
      });

      if (!response.ok) {
        throw new Error('Failed to analyze symptoms');
      }

      const data: TriageResponse = await response.json();
      setTriageResult(data);

    } catch (err: any) {
      setError(err.message || 'An error occurred during triage');
      console.error('Triage error:', err);
    } finally {
      setIsLoading(false);
    }
  }, [messages]);

  return {
    messages,
    isLoading,
    isEmergency,
    triageReady,
    triageResult,
    error,
    sendMessage,
    analyzeSymptoms
  };
}
