import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area } from 'recharts';
import { Download, TrendingUp, Activity } from 'lucide-react';

const data = [
  { name: 'Mon', sleep: 7, stress: 4, energy: 6 },
  { name: 'Tue', sleep: 6.5, stress: 5, energy: 7 },
  { name: 'Wed', sleep: 8, stress: 3, energy: 8 },
  { name: 'Thu', sleep: 7.5, stress: 4, energy: 8 },
  { name: 'Fri', sleep: 6, stress: 6, energy: 5 },
  { name: 'Sat', sleep: 9, stress: 2, energy: 9 },
  { name: 'Sun', sleep: 8.5, stress: 2, energy: 8 },
];

const Reports = () => {
  return (
    <div className="space-y-8 animate-in fade-in duration-500 pb-10">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-slate-800">Weekly Report</h1>
          <p className="text-slate-500 mt-2">Your health and wellness summary for the past 7 days.</p>
        </div>
        <button className="px-4 py-2.5 bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 hover:text-primary-600 rounded-xl font-medium shadow-sm transition-all flex items-center justify-center gap-2">
          <Download size={18} /> Download PDF
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="glass-card p-6">
          <div className="flex items-center gap-2 mb-6">
            <div className="p-2 bg-indigo-50 text-indigo-500 rounded-lg">
              <Activity size={20} />
            </div>
            <h2 className="text-lg font-bold text-slate-800">Energy & Sleep</h2>
          </div>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={data}>
                <defs>
                  <linearGradient id="colorEnergy" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="colorSleep" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{fill: '#64748b'}} />
                <YAxis axisLine={false} tickLine={false} tick={{fill: '#64748b'}} />
                <Tooltip 
                  contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                />
                <Area type="monotone" dataKey="energy" stroke="#3b82f6" fillOpacity={1} fill="url(#colorEnergy)" />
                <Area type="monotone" dataKey="sleep" stroke="#8b5cf6" fillOpacity={1} fill="url(#colorSleep)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="glass-card p-6">
          <div className="flex items-center gap-2 mb-6">
            <div className="p-2 bg-rose-50 text-rose-500 rounded-lg">
              <TrendingUp size={20} />
            </div>
            <h2 className="text-lg font-bold text-slate-800">Stress Levels</h2>
          </div>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={data}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{fill: '#64748b'}} />
                <YAxis axisLine={false} tickLine={false} tick={{fill: '#64748b'}} />
                <Tooltip 
                  contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                />
                <Line type="monotone" dataKey="stress" stroke="#f43f5e" strokeWidth={3} dot={{ r: 4, strokeWidth: 2 }} activeDot={{ r: 6 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      <div className="glass-card p-6">
        <h2 className="text-lg font-bold text-slate-800 mb-4">Symptom Summary</h2>
        <div className="space-y-4">
          <p className="text-slate-600 leading-relaxed">
            Overall wellness has improved compared to last week. You reported minor headaches on Tuesday (Stress Level: 5) but your sleep improved significantly towards the weekend, reaching peak energy on Saturday. Your hydration levels are consistent with your goals.
          </p>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-4">
            <div className="p-4 bg-slate-50 rounded-xl">
              <p className="text-sm font-medium text-slate-500">Avg Sleep</p>
              <p className="text-2xl font-bold text-slate-800">7.5 hrs</p>
            </div>
            <div className="p-4 bg-slate-50 rounded-xl">
              <p className="text-sm font-medium text-slate-500">Energy Score</p>
              <p className="text-2xl font-bold text-slate-800">7.2/10</p>
            </div>
            <div className="p-4 bg-slate-50 rounded-xl">
              <p className="text-sm font-medium text-slate-500">Meds Taken</p>
              <p className="text-2xl font-bold text-slate-800">95%</p>
            </div>
            <div className="p-4 bg-slate-50 rounded-xl">
              <p className="text-sm font-medium text-slate-500">Stress Avg</p>
              <p className="text-2xl font-bold text-slate-800">3.7/10</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Reports;
