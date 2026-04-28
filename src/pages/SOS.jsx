import React, { useState, useEffect } from 'react';
import { Phone, AlertTriangle, Save } from 'lucide-react';

const SOS = () => {
  const [emergencyNumber, setEmergencyNumber] = useState('');
  const [savedNumber, setSavedNumber] = useState('');
  const [showConfirm, setShowConfirm] = useState(false);

  useEffect(() => {
    const number = localStorage.getItem('auracare_emergency_number');
    if (number) {
      setEmergencyNumber(number);
      setSavedNumber(number);
    }
  }, []);

  const handleSave = () => {
    if (emergencyNumber) {
      localStorage.setItem('auracare_emergency_number', emergencyNumber);
      setSavedNumber(emergencyNumber);
      alert('Emergency number saved!');
    }
  };

  const handleSOSClick = () => {
    if (!savedNumber) {
      alert('Please save an emergency contact number first.');
      return;
    }
    setShowConfirm(true);
  };

  const confirmCall = () => {
    setShowConfirm(false);
    window.location.href = `tel:${savedNumber}`;
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-500 max-w-2xl mx-auto">
      <div className="text-center">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-red-100 text-red-500 mb-4 animate-pulse">
          <AlertTriangle size={32} />
        </div>
        <h1 className="text-3xl font-bold text-slate-800">SOS Emergency</h1>
        <p className="text-slate-500 mt-2">One-tap access to your emergency contact.</p>
      </div>

      <div className="glass-card p-8 flex flex-col items-center">
        {showConfirm ? (
          <div className="text-center space-y-6 animate-in zoom-in duration-300">
            <h2 className="text-2xl font-bold text-slate-800">Call Emergency Contact?</h2>
            <p className="text-slate-600">You are about to call: <span className="font-bold text-slate-800">{savedNumber}</span></p>
            <div className="flex gap-4 justify-center">
              <button 
                onClick={() => setShowConfirm(false)}
                className="px-6 py-3 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl font-medium transition-colors"
              >
                Cancel
              </button>
              <button 
                onClick={confirmCall}
                className="px-6 py-3 bg-red-500 hover:bg-red-600 text-white rounded-xl font-medium shadow-md shadow-red-500/20 transition-colors flex items-center gap-2"
              >
                <Phone size={20} /> Yes, Call Now
              </button>
            </div>
          </div>
        ) : (
          <button
            onClick={handleSOSClick}
            className="w-48 h-48 rounded-full bg-gradient-to-b from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 text-white shadow-[0_0_40px_rgba(239,68,68,0.4)] hover:shadow-[0_0_60px_rgba(239,68,68,0.6)] hover:scale-105 active:scale-95 transition-all duration-300 flex flex-col items-center justify-center border-4 border-red-400 group"
          >
            <AlertTriangle size={48} className="mb-2 group-hover:animate-bounce" />
            <span className="text-3xl font-black tracking-widest">SOS</span>
          </button>
        )}
      </div>

      <div className="glass-card p-6">
        <h2 className="text-lg font-bold text-slate-800 mb-4 flex items-center gap-2">
          <Phone size={20} className="text-slate-400" /> Emergency Configuration
        </h2>
        
        <div className="flex flex-col sm:flex-row gap-4">
          <input
            type="tel"
            value={emergencyNumber}
            onChange={(e) => setEmergencyNumber(e.target.value)}
            placeholder="Enter emergency phone number"
            className="flex-1 px-4 py-3 rounded-xl border border-slate-200 bg-white focus:border-primary-400 focus:ring-2 focus:ring-primary-100 outline-none transition-all"
          />
          <button
            onClick={handleSave}
            className="px-6 py-3 bg-primary-500 hover:bg-primary-600 text-white rounded-xl font-medium shadow-md transition-colors flex items-center justify-center gap-2 whitespace-nowrap"
          >
            <span className="hidden sm:inline">Save Contact</span>
            <span className="sm:hidden">Save</span> <Save size={18} />
          </button>
        </div>
        {savedNumber && (
          <p className="text-sm text-green-600 mt-3 flex items-center gap-1">
            ✓ Currently saved: {savedNumber}
          </p>
        )}
      </div>
    </div>
  );
};

export default SOS;
