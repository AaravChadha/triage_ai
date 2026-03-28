import React from 'react';
import { FileText, AlertCircle } from 'lucide-react';

interface SummaryData {
  chief_complaint: string;
  symptoms: string[];
  duration: string;
  pain_level: number;
  relevant_history: string;
  severity: string;
  recommended_care: string;
  ai_notes: string;
}

interface PatientSummaryProps {
  summary: SummaryData;
  onSendToFacility: () => void;
  isSending: boolean;
  sent: boolean;
}

export function PatientSummary({ summary, onSendToFacility, isSending, sent }: PatientSummaryProps) {
  return (
    <div className="w-full max-w-2xl bg-white rounded-2xl shadow-lg border border-gray-200 overflow-hidden">
      <div className="bg-gray-900 text-white px-6 py-4 flex items-center">
        <FileText size={20} className="mr-3" />
        <h2 className="text-lg font-bold">Pre-Arrival Patient Summary</h2>
      </div>

      <div className="p-6 space-y-4">
        <div>
          <h3 className="text-xs font-semibold text-gray-400 uppercase tracking-wider">Chief Complaint</h3>
          <p className="text-gray-900 font-medium mt-1">{summary.chief_complaint}</p>
        </div>

        <div>
          <h3 className="text-xs font-semibold text-gray-400 uppercase tracking-wider">Symptoms</h3>
          <ul className="mt-1 space-y-1">
            {summary.symptoms.map((s, i) => (
              <li key={i} className="text-gray-700 text-sm flex items-start">
                <span className="text-gray-400 mr-2">•</span>{s}
              </li>
            ))}
          </ul>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <h3 className="text-xs font-semibold text-gray-400 uppercase tracking-wider">Duration</h3>
            <p className="text-gray-900 mt-1">{summary.duration}</p>
          </div>
          <div>
            <h3 className="text-xs font-semibold text-gray-400 uppercase tracking-wider">Pain Level</h3>
            <p className="text-gray-900 mt-1">{summary.pain_level}/10</p>
          </div>
        </div>

        <div>
          <h3 className="text-xs font-semibold text-gray-400 uppercase tracking-wider">Relevant History</h3>
          <p className="text-gray-700 text-sm mt-1">{summary.relevant_history}</p>
        </div>

        <div>
          <h3 className="text-xs font-semibold text-gray-400 uppercase tracking-wider">Severity Classification</h3>
          <p className="text-gray-900 font-semibold mt-1">{summary.severity}</p>
        </div>

        <div>
          <h3 className="text-xs font-semibold text-gray-400 uppercase tracking-wider">Recommended Care</h3>
          <p className="text-gray-700 text-sm mt-1">{summary.recommended_care}</p>
        </div>

        <div className="bg-amber-50 border border-amber-200 rounded-xl p-4">
          <div className="flex items-start">
            <AlertCircle size={16} className="text-amber-500 mr-2 mt-0.5 flex-shrink-0" />
            <div>
              <h3 className="text-xs font-semibold text-amber-600 uppercase tracking-wider">AI Assessment</h3>
              <p className="text-gray-700 text-sm mt-1">{summary.ai_notes}</p>
            </div>
          </div>
        </div>
      </div>

      <div className="px-6 pb-6">
        {!sent ? (
          <button
            onClick={onSendToFacility}
            disabled={isSending}
            className="w-full bg-blue-600 text-white font-bold py-3 rounded-xl shadow-lg shadow-blue-500/20 hover:bg-blue-700 active:scale-[0.98] transition-all disabled:opacity-50"
          >
            {isSending ? 'Sending...' : 'Send to Facility'}
          </button>
        ) : (
          <div className="w-full bg-green-50 text-green-700 font-semibold py-3 rounded-xl text-center border border-green-200">
            Summary sent successfully
          </div>
        )}
      </div>
    </div>
  );
}
