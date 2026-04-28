import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import {
  Activity,
  ShieldAlert,
  Pill,
  Clock,
  Plus,
  Edit2,
  Trash2,
  Timer,
  Mic,
  Sparkles,
  CheckCircle2,
  Loader2,
  MessageSquare,
  ChevronRight,
} from "lucide-react";
import api from "../utils/api";
import MedicineModal from "../components/MedicineModal";
import { useAlarm } from "../context/AlarmContext";

const Dashboard = () => {
  const { user } = useAuth();
  const { refreshMedicines } = useAlarm();
  const navigate = useNavigate();
  const [medicines, setMedicines] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedMedicine, setSelectedMedicine] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showToast, setShowToast] = useState(false);

  useEffect(() => {
    fetchMedicines();
  }, []);

  const fetchMedicines = async () => {
    try {
      setLoading(true);
      const { data } = await api.get("/api/medicines/today");
      setMedicines(data);
    } catch (error) {
      console.error("Error fetching medicines:", error);
    } finally {
      setLoading(false);
    }
  };

  const onMedicineSaved = () => {
    fetchMedicines();
    refreshMedicines();
    setShowToast(true);
    setTimeout(() => setShowToast(false), 3000);
  };

  const handleMarkTaken = async (id, index) => {
    try {
      const medicine = medicines.find((m) => (m._id || m.id) === id);
      if (!medicine) return;
      const takenStatus =
        medicine.takenStatus?.map((s, i) => (i === index ? true : s)) ||
        medicine.time.map((_) => false);
      await api.patch(`/api/medicines/${id}`, { takenStatus });
      fetchMedicines();
    } catch (error) {
      console.error("Error marking taken:", error);
    }
  };

  const handleDelete = async (id) => {
    if (!id) {
      console.error("No medicine ID provided for deletion");
      return;
    }

    if (window.confirm("Are you sure you want to delete this reminder?")) {
      try {
        await api.delete(`/api/medicines/${id}`);
        // Immediately update local state for better responsiveness
        setMedicines(prev => prev.filter(m => (m._id || m.id) !== id));
        // Also fetch from server to ensure sync
        fetchMedicines();
        if (refreshMedicines) refreshMedicines();
      } catch (error) {
        console.error("Error deleting medicine:", error);
        alert(`Failed to delete medicine: ${error.response?.data?.detail || error.message}`);
      }
    }
  };

  const handleSnooze = async (medId, timeIndex) => {
    try {
      const medicine = medicines.find((m) => (m._id || m.id) === medId);
      if (!medicine) return;

      const newTimes = [...medicine.time];
      const [hours, minutes] = newTimes[timeIndex].split(":");
      const date = new Date();
      date.setHours(parseInt(hours), parseInt(minutes) + 15);
      newTimes[timeIndex] = `${date.getHours().toString().padStart(2, "0")}:${date.getMinutes().toString().padStart(2, "0")}`;

      await api.patch(`/api/medicines/${medId}`, { time: newTimes });
      fetchMedicines();
    } catch (error) {
      console.error("Error snoozing medicine from dashboard:", error);
    }
  };

  return (
    <div className="space-y-10 animate-in fade-in slide-in-from-bottom-6 duration-1000 pb-16 relative">
      <MedicineModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        medicine={selectedMedicine}
        onSave={onMedicineSaved}
      />

      {/* Success Toast */}
      {showToast && (
        <div className="fixed top-8 left-1/2 -translate-x-1/2 z-[100] bg-slate-900/90 backdrop-blur-md text-white px-8 py-4 rounded-3xl shadow-2xl flex items-center gap-4 animate-in fade-in slide-in-from-top-8 duration-500">
          <div className="bg-green-500 rounded-full p-1">
            <CheckCircle2 size={16} />
          </div>
          <span className="font-semibold text-sm">
            Schedule updated perfectly
          </span>
        </div>
      )}

      {/* Header section with refined typography */}
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6">
        <div>
          <h1 className="text-4xl font-bold text-slate-900 tracking-tight">
            Hello,{" "}
            <span className="text-primary-600 font-medium">{user?.name}</span>
          </h1>
          <p className="text-slate-500 mt-2 text-lg font-normal">
            Everything looks good for your health today.
          </p>
        </div>
        <button
          onClick={() => {
            setSelectedMedicine(null);
            setIsModalOpen(true);
          }}
          className="flex items-center gap-3 px-8 py-4 bg-primary-600 text-white rounded-[2rem] font-semibold hover:bg-primary-700 shadow-xl shadow-primary-200 transition-all active:scale-95 group shrink-0"
        >
          <Plus
            size={22}
            className="group-hover:rotate-90 transition-transform"
          />
          Add New Dose
        </button>
      </div>

      {/* Interactive Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="glass-card p-8 group transition-all duration-500 border-none">
          <div className="flex items-center justify-between mb-6">
            <div className="w-16 h-16 rounded-3xl bg-blue-50/50 flex items-center justify-center text-blue-500 ring-1 ring-blue-100/50">
              <Pill size={32} />
            </div>
            <div className="text-[10px] font-bold uppercase tracking-[0.2em] text-blue-400">
              Activity
            </div>
          </div>
          <p className="text-slate-500 font-medium text-sm">Daily Progress</p>
          <h3 className="text-4xl font-bold text-slate-900 mt-2 flex items-baseline gap-2">
            {medicines.filter((m) => m.takenStatus[0]).length}
            <span className="text-lg font-medium text-slate-300">
              / {medicines.length}
            </span>
          </h3>
        </div>

        <button
          onClick={() => navigate("/reports")}
          className="glass-card p-8 text-left group hover:bg-primary-50/50 hover:shadow-2xl transition-all duration-500 border-none relative overflow-hidden"
        >
          <div className="flex items-center justify-between mb-6">
            <div className="w-16 h-16 rounded-3xl bg-indigo-50/50 flex items-center justify-center text-indigo-500 ring-1 ring-indigo-100/50">
              <Activity size={32} />
            </div>
            <ChevronRight
              size={20}
              className="text-slate-300 group-hover:translate-x-1 transition-transform"
            />
          </div>
          <p className="text-slate-500 font-medium text-sm">Health Status</p>
          <h3 className="text-4xl font-bold text-slate-900 mt-2">Optimal</h3>
          <div className="mt-4 flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
            <span className="text-xs font-bold text-green-600 uppercase">
              Live Reports
            </span>
          </div>
        </button>

        <button
          onClick={() => navigate("/sos")}
          className="glass-card p-8 text-left group bg-slate-900 hover:bg-red-600 transition-all duration-500 border-none shadow-slate-200"
        >
          <div className="flex items-center justify-between mb-6">
            <div className="w-16 h-16 rounded-3xl bg-red-500/20 flex items-center justify-center text-red-500">
              <ShieldAlert size={32} />
            </div>
            <ChevronRight
              size={20}
              className="text-white/20 group-hover:translate-x-1 transition-transform"
            />
          </div>
          <p className="text-slate-400 font-medium text-sm">Emergency System</p>
          <h3 className="text-4xl font-bold text-white mt-2 tracking-tight">
            SOS Active
          </h3>
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-10">
        <div className="glass-card p-10 border-none bg-white/40">
          <div className="flex items-center justify-between mb-10">
            <h2 className="text-2xl font-bold text-slate-900 tracking-tight">
              Today's Schedule
            </h2>
            <div className="text-[10px] font-bold uppercase tracking-widest text-slate-400">
              Timeline view
            </div>
          </div>

          <div className="space-y-6">
            {loading ? (
              <div className="flex flex-col items-center py-16 gap-4">
                <Loader2
                  className="animate-spin text-primary-600/30"
                  size={40}
                />
                <p className="text-slate-400 font-medium animate-pulse">
                  Refining schedule...
                </p>
              </div>
            ) : medicines.length === 0 ? (
              <div className="text-center py-20 text-slate-400 border-2 border-dashed border-slate-100 rounded-[3rem] flex flex-col items-center gap-6">
                <div className="w-20 h-20 rounded-full bg-slate-50 flex items-center justify-center text-slate-200">
                  <Pill size={40} />
                </div>
                <p className="font-semibold text-slate-500">
                  Your medication list is empty.
                </p>
              </div>
            ) : (
              medicines.map((med) => (
                <div
                  key={med._id || med.id}
                  className="group flex items-center p-6 rounded-[2.5rem] border border-white bg-white/60 hover:bg-white hover:shadow-[0_20px_60px_-15px_rgba(0,0,0,0.05)] transition-all duration-500"
                >
                  <div
                    className={`w-1.5 h-16 rounded-full mr-6 transition-colors duration-500 ${med.takenStatus[0] ? "bg-green-400" : "bg-primary-500"}`}
                  />
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-3">
                      <h4 className="font-bold text-xl text-slate-900 truncate">
                        {med.name}
                      </h4>
                      <span className="px-3 py-1 bg-slate-100 text-slate-500 rounded-xl text-[10px] font-bold uppercase tracking-tighter shrink-0">
                        {med.dosage}
                      </span>
                    </div>
                    <p className="text-base text-slate-500 font-normal flex items-center gap-2 mt-1.5">
                      <Clock size={18} className="text-slate-300" />
                      <span className="font-medium">{med.time[0]}</span>
                      <span className="text-slate-200">|</span>
                      <span>{med.condition}</span>
                      {med.isSnoozed && (
                        <span className="ml-2 text-primary-500 font-bold flex items-center gap-1">
                          <Timer size={14} /> Ext. 15m
                        </span>
                      )}
                    </p>
                  </div>

                  <div className="flex items-center gap-4 ml-4">
                    {!med.takenStatus[0] ? (
                      <div className="flex items-center gap-3">
                        <button
                          onClick={() => handleSnooze(med._id || med.id, 0)}
                          className="w-12 h-12 flex items-center justify-center text-slate-400 hover:text-primary-600 hover:bg-primary-50 rounded-2xl transition-all"
                          title="Snooze 15m"
                        >
                          <Timer size={24} />
                        </button>
                        <button
                          onClick={() => handleMarkTaken(med._id || med.id, 0)}
                          className="px-7 py-3.5 bg-primary-600 text-white hover:bg-primary-700 rounded-[1.5rem] text-sm font-semibold shadow-lg shadow-primary-100 transition-all active:scale-95"
                        >
                          Mark Done
                        </button>
                      </div>
                    ) : (
                      <div className="px-5 py-2.5 bg-green-50 text-green-600 rounded-[1.5rem] text-xs font-bold leading-none tracking-tight flex items-center gap-2 ring-1 ring-green-200">
                        <CheckCircle2 size={16} /> COMPLETED
                      </div>
                    )}
                    <div className="flex opacity-40 group-hover:opacity-100 transition-all gap-1 translate-x-4 group-hover:translate-x-0">
                      <button
                        onClick={() => {
                          setSelectedMedicine(med);
                          setIsModalOpen(true);
                        }}
                        className="p-3 text-slate-300 hover:text-blue-500 hover:bg-blue-50 rounded-2xl transition-all"
                      >
                        <Edit2 size={20} />
                      </button>
                      <button
                        onClick={() => handleDelete(med._id || med.id)}
                        className="p-3 text-slate-300 hover:text-red-500 hover:bg-red-50 rounded-2xl transition-all"
                      >
                        <Trash2 size={20} />
                      </button>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Premium AI Solutions Hub */}
        <div className="glass-card p-10 bg-gradient-to-br from-blue-50/80 to-indigo-50/80 border-none relative overflow-hidden group">
          <div className="absolute -top-12 -right-12 w-64 h-64 bg-primary-600/5 rounded-full blur-[100px] group-hover:bg-primary-600/10 transition-all duration-1000" />
          <div className="absolute -bottom-12 -left-12 w-64 h-64 bg-blue-600/5 rounded-full blur-[100px] group-hover:bg-blue-600/10 transition-all duration-1000" />

          <div className="relative z-10 h-full flex flex-col items-center text-center">
            <div className="w-20 h-20 rounded-[2rem] bg-indigo-500/10 flex items-center justify-center text-indigo-600 mb-8 border border-indigo-200/50 shadow-inner">
              <Sparkles size={40} className="animate-pulse" />
            </div>
            <h2 className="text-3xl font-bold text-blue-950 tracking-tight mb-4">
              Health Solution AI
            </h2>
            <p className="text-blue-800 text-lg font-medium leading-relaxed max-w-sm mb-12">
              "Ask me anything about your current medication or any health
              issues you're facing."
            </p>

            <div className="w-full grid grid-cols-1 gap-4 text-left">
              <div className="p-6 bg-white/60 rounded-3xl border border-blue-100/50 hover:bg-white/80 hover:shadow-xl hover:shadow-blue-500/5 transition-all duration-300 group/item">
                <p className="text-blue-500 text-[10px] font-bold uppercase tracking-[0.2em] mb-2 group-hover/item:text-primary-600 transition-colors">
                  Example Query
                </p>
                <p className="text-blue-900 text-base font-semibold">
                  "What should I do for a sudden migraine?"
                </p>
              </div>
              <div className="p-6 bg-white/60 rounded-3xl border border-blue-100/50 hover:bg-white/80 hover:shadow-xl hover:shadow-blue-500/5 transition-all duration-300 group/item">
                <p className="text-blue-500 text-[10px] font-bold uppercase tracking-[0.2em] mb-2 group-hover/item:text-primary-600 transition-colors">
                  Health Tip
                </p>
                <p className="text-blue-900 text-base font-semibold">
                  "Stay hydrated and avoid bright screens."
                </p>
              </div>
            </div>

            <div className="mt-auto pt-10 flex items-center gap-3 text-blue-400 text-xs font-bold uppercase tracking-widest">
              <MessageSquare size={16} />
              <span>AI Core Online</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
