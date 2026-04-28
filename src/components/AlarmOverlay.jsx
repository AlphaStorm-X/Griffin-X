import React from 'react';
import { useAlarm } from '../context/AlarmContext';
import { Pill, Clock, Bell, Trash2, CheckCircle2, Timer, X } from 'lucide-react';

const AlarmOverlay = () => {
  const { activeAlarm, stopAlarm, markAsTaken, snoozeAlarm } = useAlarm();

  if (!activeAlarm) return null;

  return (
    <div className="fixed inset-0 z-[200] flex items-center justify-center p-6 bg-slate-900/40 backdrop-blur-2xl animate-in fade-in duration-700">
      <div className="absolute inset-0 bg-gradient-to-t from-primary-900/20 to-transparent pointer-events-none" />
      
      <div className="bg-white rounded-[3rem] w-full max-w-lg overflow-hidden shadow-[0_32px_128px_-16px_rgba(0,0,0,0.3)] animate-in zoom-in-95 slide-in-from-bottom-12 duration-700 border border-white relative">
        {/* Animated Background Pulse */}
        <div className="absolute -top-24 -right-24 w-64 h-64 bg-primary-100 rounded-full blur-[80px] animate-pulse" />
        <div className="absolute -bottom-24 -left-24 w-64 h-64 bg-indigo-100 rounded-full blur-[80px] animate-pulse delay-700" />

        <div className="p-10 relative z-10 flex flex-col items-center text-center">
            {/* Alarm Icon */}
            <div className="relative mb-8">
                <div className="absolute inset-0 bg-primary-500 rounded-full animate-ping opacity-20 scale-150" />
                <div className="w-24 h-24 rounded-[2.5rem] bg-primary-600 text-white flex items-center justify-center shadow-2xl shadow-primary-200 relative z-10">
                    <Bell size={44} className="animate-bounce" />
                </div>
            </div>

            <p className="text-primary-600 text-xs font-bold uppercase tracking-[0.3em] mb-3">Time for Medication</p>
            <h2 className="text-5xl font-extrabold text-slate-900 tracking-tight mb-2 leading-none">{activeAlarm.name}</h2>
            <div className="flex items-center gap-3 mb-10">
                <span className="px-4 py-1.5 bg-slate-100 text-slate-500 rounded-2xl text-sm font-bold uppercase tracking-tight">{activeAlarm.dosage}</span>
                <span className="text-slate-300 font-light text-2xl">/</span>
                <div className="flex items-center gap-2 text-slate-600 font-semibold group">
                    <Clock size={18} className="text-primary-400 group-hover:rotate-12 transition-transform" />
                    {activeAlarm.time[activeAlarm.timeIndex]}
                </div>
            </div>

            <div className="w-full space-y-4 mb-8">
                <div className="p-6 bg-slate-50/50 rounded-[2rem] border border-slate-100 flex items-center gap-5 group hover:bg-white hover:shadow-xl transition-all duration-500">
                    <div className="w-12 h-12 rounded-2xl bg-white shadow-sm flex items-center justify-center text-primary-500 group-hover:scale-110 transition-transform">
                        <Pill size={24} />
                    </div>
                    <div className="text-left">
                        <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Instruction</p>
                        <p className="text-slate-700 font-bold text-xl leading-tight">Take {activeAlarm.condition}</p>
                    </div>
                </div>
            </div>

            <div className="grid grid-cols-1 w-full gap-4">
                <button 
                  onClick={markAsTaken}
                  className="w-full py-6 bg-primary-600 text-white rounded-[2rem] font-bold text-lg hover:bg-primary-700 shadow-xl shadow-primary-200 transition-all active:scale-95 flex items-center justify-center gap-3 group"
                >
                    <CheckCircle2 size={24} className="group-hover:scale-125 transition-transform" />
                    Mark as Taken
                </button>
                
                <div className="grid grid-cols-2 gap-4">
                    <button 
                        onClick={() => snoozeAlarm(15)}
                        className="py-5 bg-white border-2 border-slate-100 text-slate-600 rounded-[2rem] font-bold hover:bg-slate-50 transition-all active:scale-95 flex items-center justify-center gap-2 group"
                    >
                        <Timer size={20} className="text-primary-500 group-hover:rotate-[-10deg] transition-transform" />
                        Snooze 15m
                    </button>
                    <button 
                        onClick={stopAlarm}
                        className="py-5 bg-slate-100 text-slate-500 rounded-[2rem] font-bold hover:bg-slate-200 transition-all active:scale-95 flex items-center justify-center gap-2 group"
                    >
                        <X size={20} className="group-hover:scale-110 transition-transform" />
                        Dismiss
                    </button>
                </div>
            </div>
        </div>
      </div>
    </div>
  );
};

export default AlarmOverlay;
