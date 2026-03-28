
import { Facility } from '../types';
import { MapPin, Clock, Navigation, CheckCircle2 } from 'lucide-react';

export function FacilityList({ facilities }: { facilities: Facility[] }) {
  if (!facilities.length) return null;

  return (
    <div className="w-full max-w-2xl mt-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <h2 className="text-2xl font-bold tracking-tight text-gray-900 mb-4">Nearby Recommended Facilities</h2>
      <div className="space-y-4">
        {facilities.map((fac, idx) => (
          <div 
            key={idx} 
            className={`relative p-6 rounded-3xl border shadow-sm transition-all hover:shadow-md bg-white ${fac.is_recommended ? 'border-teal-400 ring-2 ring-teal-400' : 'border-gray-200'}`}
          >
            {fac.is_recommended && (
              <div className="absolute -top-3 left-6 px-3 py-1 bg-teal-500 text-white text-xs font-bold uppercase tracking-wider rounded-full shadow-sm flex items-center">
                <CheckCircle2 size={12} className="mr-1" /> Recommended
              </div>
            )}
            
            <div className="flex justify-between items-start">
              <div className="pr-4">
                <h3 className="text-lg font-bold text-gray-900">{fac.name}</h3>
                <div className="flex items-center text-gray-500 mt-1">
                  <MapPin size={14} className="mr-1 flex-shrink-0" />
                  <span className="text-sm font-medium">{fac.address} • {fac.distance_miles} mi</span>
                </div>
              </div>
              <div className="flex flex-col items-end flex-shrink-0">
                <div className="flex flex-col items-end bg-gray-50 rounded-xl px-3 py-2 border border-gray-100">
                  <span className="text-xs font-bold text-gray-400 uppercase tracking-wide flex items-center mb-1">
                    <Clock size={12} className="mr-1" /> Wait Time
                  </span>
                  <span className="text-sm font-semibold text-gray-900 text-right">{fac.wait_time}</span>
                </div>
              </div>
            </div>
            
            <div className="mt-5 pt-4 border-t border-gray-100 flex justify-end">
              <a 
                href={fac.maps_url} 
                target="_blank" 
                rel="noopener noreferrer"
                className="inline-flex items-center px-4 py-2 bg-blue-50 text-blue-700 font-semibold rounded-xl text-sm hover:bg-blue-100 transition-colors"
               >
                 <Navigation size={14} className="mr-2" />
                 Directions
              </a>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
