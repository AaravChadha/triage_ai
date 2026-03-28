import React from 'react';
import { useChat } from './hooks/useChat';
import { ChatWindow } from './components/ChatWindow';
import { EmergencyAlert } from './components/EmergencyAlert';
import { TriageResult } from './components/TriageResult';
import { Activity } from 'lucide-react';

export default function App() {
  const {
    messages,
    isLoading,
    isEmergency,
    triageReady,
    triageResult,
    error,
    sendMessage,
    analyzeSymptoms
  } = useChat();

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center py-12 px-4 selection:bg-blue-100 selection:text-blue-900 font-sans">
      {isEmergency && <EmergencyAlert />}

      <div className="mb-8 flex items-center">
         <div className="bg-blue-600 p-3 rounded-2xl shadow-lg mr-4">
            <Activity className="text-white h-8 w-8" />
         </div>
         <div>
            <h1 className="text-3xl font-extrabold text-gray-900 tracking-tight">AI Pre-Arrival Triage</h1>
            <p className="text-gray-500 font-medium">Smart routing to the right level of care.</p>
         </div>
      </div>

      {!triageResult ? (
        <>
          <ChatWindow 
            messages={messages}
            isLoading={isLoading}
            onSendMessage={sendMessage}
            error={error}
          />
          
          {triageReady && (
            <button
              onClick={analyzeSymptoms}
              disabled={isLoading}
              className="mt-6 px-8 py-4 bg-gray-900 text-white rounded-full font-bold shadow-xl shadow-gray-900/20 hover:bg-gray-800 hover:scale-105 active:scale-95 transition-all disabled:opacity-50 flex items-center space-x-2"
            >
              <span>Analyze My Symptoms</span>
              {isLoading && <span className="animate-pulse ml-2">...</span>}
            </button>
          )}
        </>
      ) : (
        <React.Fragment>
          <TriageResult result={triageResult} />
          <button
              onClick={() => window.location.reload()}
              className="mt-8 text-gray-500 font-medium hover:text-gray-900 underline decoration-dotted transition-colors"
          >
              Start specific session over
          </button>
        </React.Fragment>
      )}
    </div>
  );
}
