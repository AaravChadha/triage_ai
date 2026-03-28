import React from 'react';
import { TriageResponse } from '../types';
import { Activity, Clock, ShieldAlert, CheckCircle2 } from 'lucide-react';

export function TriageResult({ result }: { result: TriageResponse }) {
  let color = "bg-blue-50 text-blue-700 border-blue-200";
  let icon = <CheckCircle2 className="text-blue-500" />;
  let badgeColor = "bg-blue-100 text-blue-700";

  switch (result.required_tier) {
    case 1:
      color = "bg-red-50 text-red-800 border-red-200";
      icon = <ShieldAlert className="text-red-600" />;
      badgeColor = "bg-red-100 text-red-800";
      break;
    case 2:
      color = "bg-orange-50 text-orange-800 border-orange-200";
      icon = <Activity className="text-orange-600" />;
      badgeColor = "bg-orange-100 text-orange-800";
      break;
    case 3:
      color = "bg-yellow-50 text-yellow-800 border-yellow-200";
      icon = <CheckCircle2 className="text-yellow-600" />;
      badgeColor = "bg-yellow-100 text-yellow-800";
      break;
    case 4:
    case 5:
      color = "bg-green-50 text-green-800 border-green-200";
      icon = <CheckCircle2 className="text-green-600" />;
      badgeColor = "bg-green-100 text-green-800";
      break;
  }

  return (
    <div className={`w-full max-w-2xl border rounded-3xl p-8 shadow-xl ${color} bg-white flex flex-col mt-4 animate-in fade-in slide-in-from-bottom-4 duration-500`}>
      <div className="flex items-center space-x-4 mb-6 pb-6 border-b border-gray-100/10">
        <div className={`p-4 rounded-2xl shadow-sm ${badgeColor}`}>
          {icon}
        </div>
        <div>
          <h2 className="text-2xl font-bold tracking-tight text-gray-900">Recommended Care</h2>
          <p className={`font-semibold text-lg mt-1 tracking-wide ${color.split(' ')[1]}`}>
             Level: {result.severity.replace(/_/g, ' ').toUpperCase()}
          </p>
        </div>
      </div>

      <div className="space-y-6">
        <div>
          <h3 className="text-sm font-bold text-gray-500 uppercase tracking-wider mb-2">Reasoning</h3>
          <p className="text-gray-800 leading-relaxed font-medium">{result.reasoning}</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
           <div className="bg-gray-50/50 border border-gray-100 p-5 rounded-2xl">
             <h3 className="text-sm font-bold text-gray-500 uppercase tracking-wider mb-3">Key Symptoms</h3>
             <ul className="list-disc leading-relaxed text-gray-800 pl-4 font-medium space-y-1">
               {result.key_symptoms.map((s, i) => <li key={i}>{s}</li>)}
             </ul>
           </div>
           
           <div className="bg-gray-50/50 border border-gray-100 p-5 rounded-2xl flex flex-col justify-between">
             <div>
               <h3 className="text-sm font-bold text-gray-500 uppercase tracking-wider mb-3 flex items-center">
                 <Clock size={16} className="mr-2" />
                 Est. Duration
               </h3>
               <p className="font-semibold text-gray-800">{result.estimated_duration}</p>
             </div>
             <div className="mt-4">
                <p className="text-xs text-gray-400 font-bold tracking-widest uppercase">Confidence</p>
                <div className="flex items-center mt-1">
                   <div className="w-full bg-gray-200 rounded-full h-2.5 mr-3">
                     <div className="bg-gray-800 h-2.5 rounded-full" style={{ width: `${Math.round(result.confidence * 100)}%` }}></div>
                   </div>
                   <span className="text-sm font-bold text-gray-700">{Math.round(result.confidence * 100)}%</span>
                </div>
             </div>
           </div>
        </div>

        {result.flags.length > 0 && (
          <div className="bg-orange-50/50 border border-orange-100 p-5 rounded-2xl">
            <h3 className="text-sm font-bold text-orange-800 uppercase tracking-wider mb-2">Clinical Flags</h3>
            <ul className="list-disc leading-relaxed text-orange-900 pl-4 font-medium space-y-1">
              {result.flags.map((f, i) => <li key={i}>{f}</li>)}
            </ul>
          </div>
        )}
      </div>

    </div>
  );
}
