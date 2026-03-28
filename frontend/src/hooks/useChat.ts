import { useState, useCallback } from 'react';
import { Message, ChatResponse, TriageResponse, SummaryResponse, Facility, FacilitiesResponse } from '../types';

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isEmergency, setIsEmergency] = useState(false);
  const [emergencyReasoning, setEmergencyReasoning] = useState<string | null>(null);
  const [triageReady, setTriageReady] = useState(false);
  const [triageResult, setTriageResult] = useState<TriageResponse | null>(null);
  const [summaryResult, setSummaryResult] = useState<SummaryResponse | null>(null);
  const [facilities, setFacilities] = useState<Facility[] | null>(null);
  const [isLoadingFacilities, setIsLoadingFacilities] = useState(false);
  const [isSending, setIsSending] = useState(false);
  const [sent, setSent] = useState(false);
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
         setEmergencyReasoning(data.emergency_reasoning || null);
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

      const fetchFacilities = async (lat: number, lng: number) => {
        setIsLoadingFacilities(true);
        try {
          const facRes = await fetch(`${API_BASE_URL}/facilities`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              triage_level: data.required_tier,
              lat,
              lng,
              required_capabilities: data.required_capabilities
            })
          });
          if (facRes.ok) {
            const facData: FacilitiesResponse = await facRes.json();
            setFacilities(facData.facilities);
          }
        } catch (err) {
          console.error('Failed to fetch facilities', err);
        } finally {
          setIsLoadingFacilities(false);
        }
      };

      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          (pos) => fetchFacilities(pos.coords.latitude, pos.coords.longitude),
          (err) => {
            console.error('Geolocation error, using default Purdue Indy coordinates', err);
            fetchFacilities(39.7739, -86.1661);
          }
        );
      } else {
        fetchFacilities(39.7739, -86.1661);
      }

      // Auto-fetch summary after triage
      const summaryRes = await fetch(`${API_BASE_URL}/summary`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          history: messages,
          triage_result: data
        })
      });

      if (summaryRes.ok) {
        const summaryData: SummaryResponse = await summaryRes.json();
        setSummaryResult(summaryData);
      }

    } catch (err: any) {
      setError(err.message || 'An error occurred during triage');
      console.error('Triage error:', err);
    } finally {
      setIsLoading(false);
    }
  }, [messages]);

  const sendToFacility = useCallback(async (facilityName: string) => {
    if (!summaryResult) return;
    setIsSending(true);

    try {
      const response = await fetch(`${API_BASE_URL}/notify`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          summary: summaryResult,
          facility_name: facilityName
        })
      });

      if (response.ok) {
        setSent(true);
      }
    } catch (err: any) {
      setError(err.message || 'Failed to send summary');
    } finally {
      setIsSending(false);
    }
  }, [summaryResult]);

  const dismissEmergency = useCallback(() => {
    setIsEmergency(false);
  }, []);

  return {
    messages,
    isLoading,
    isEmergency,
    emergencyReasoning,
    triageReady,
    triageResult,
    summaryResult,
    facilities,
    isLoadingFacilities,
    isSending,
    sent,
    error,
    sendMessage,
    analyzeSymptoms,
    sendToFacility,
    dismissEmergency
  };
}
