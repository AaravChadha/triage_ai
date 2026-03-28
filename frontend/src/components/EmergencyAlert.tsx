import React, { useState } from 'react';
import { PhoneCall, AlertTriangle, HelpCircle } from 'lucide-react';

interface EmergencyAlertProps {
  onDismiss: () => void;
  reasoning?: string | null;
}

export function EmergencyAlert({ onDismiss, reasoning }: EmergencyAlertProps) {
  const [showReasoning, setShowReasoning] = useState(false);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-red-600/95 backdrop-blur-sm p-4">
       <div className="bg-white max-w-md w-full rounded-3xl p-8 flex flex-col items-center text-center shadow-2xl animate-in fade-in zoom-in duration-300">
          <div className="bg-red-100 text-red-600 p-6 rounded-full mb-6 relative">
            <div className="absolute inset-0 bg-red-100 rounded-full animate-ping opacity-75"></div>
            <AlertTriangle size={48} className="relative z-10 text-red-600" />
          </div>

          <h1 className="text-3xl font-extrabold text-gray-900 mb-2">MEDICAL EMERGENCY</h1>
          <p className="text-red-600 font-semibold text-lg mb-6">Call 911 immediately.</p>

          <p className="text-gray-600 mb-8 font-medium">
            Based on your responses, you may be experiencing a life-threatening medical emergency. Do not wait.
          </p>

          <a
            href="tel:911"
            className="w-full bg-red-600 text-white font-bold text-xl py-4 rounded-2xl shadow-lg shadow-red-500/30 hover:bg-red-700 transition-colors flex items-center justify-center flex-row"
          >
            <PhoneCall size={24} className="mr-3" />
            CALL 911 NOW
          </a>

          {reasoning && (
            <>
              <button
                className="mt-4 text-gray-500 font-medium text-sm hover:text-gray-700 transition-colors flex items-center"
                onClick={() => setShowReasoning(!showReasoning)}
              >
                <HelpCircle size={16} className="mr-1" />
                {showReasoning ? 'Hide reasoning' : 'Why is this an emergency?'}
              </button>

              {showReasoning && (
                <p className="mt-3 text-gray-600 text-sm bg-red-50 rounded-xl p-4 text-left">
                  {reasoning}
                </p>
              )}
            </>
          )}

          <button
            className="mt-4 text-gray-400 font-medium text-sm hover:text-gray-600 transition-colors underline decoration-dotted underline-offset-4"
            onClick={onDismiss}
          >
            This is not an emergency — continue chat
          </button>
       </div>
    </div>
  );
}
