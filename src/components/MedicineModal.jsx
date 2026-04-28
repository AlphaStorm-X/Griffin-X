import React, { useState, useEffect } from "react";
import { X, Clock, Calendar, Pill } from "lucide-react";
import api from "../utils/api";

const MedicineModal = ({ isOpen, onClose, medicine, onSave }) => {
  const [formData, setFormData] = useState({
    name: "",
    dosage: "",
    time: ["08:00"],
    condition: "after food",
    dateStart: new Date().toISOString().split("T")[0],
    dateEnd: new Date().toISOString().split("T")[0],
  });

  useEffect(() => {
    if (medicine) {
      setFormData({
        name: medicine.name || "",
        dosage: medicine.dosage || "",
        time: medicine.time || ["08:00"],
        condition: medicine.condition || "after food",
        dateStart: medicine.dateStart
          ? new Date(medicine.dateStart).toISOString().split("T")[0]
          : "",
        dateEnd: medicine.dateEnd
          ? new Date(medicine.dateEnd).toISOString().split("T")[0]
          : "",
      });
    } else {
      setFormData({
        name: "",
        dosage: "",
        time: ["08:00"],
        condition: "after food",
        dateStart: new Date().toISOString().split("T")[0],
        dateEnd: new Date().toISOString().split("T")[0],
      });
    }
  }, [medicine, isOpen]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    const payload = {
      ...formData,
    };

    try {
      const medicineId = medicine?._id || medicine?.id;
      if (medicineId) {
        await api.patch(`/api/medicines/${medicineId}`, payload);
      } else {
        await api.post("/api/medicines", payload);
      }
      onSave();
      onClose();
    } catch (error) {
      console.error("Error saving medicine:", error);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[120] flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-md animate-in fade-in duration-500">
      <div className="bg-white rounded-[2.5rem] w-full max-w-lg overflow-hidden shadow-2xl animate-in zoom-in-95 duration-500 border border-white">
        <div className="p-8 border-b border-slate-50 flex items-center justify-between bg-primary-50/20">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-2xl bg-primary-100 text-primary-600 flex items-center justify-center">
              <Pill size={24} />
            </div>
            <h2 className="text-2xl font-bold text-slate-900 tracking-tight">
              {medicine ? "Edit Medicine" : "New Reminder"}
            </h2>
          </div>
          <button
            onClick={onClose}
            className="p-3 hover:bg-white rounded-2xl transition-all shadow-sm"
          >
            <X size={24} className="text-slate-400" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-8 space-y-6">
          <div className="space-y-2">
            <label className="text-xs font-bold text-slate-400 uppercase tracking-widest ml-1">
              Medicine Name
            </label>
            <input
              type="text"
              required
              className="w-full px-6 py-4 rounded-2xl border border-slate-100 focus:ring-4 focus:ring-primary-50 focus:border-primary-300 outline-none transition-all text-slate-800 font-medium placeholder:text-slate-300"
              placeholder="e.g. Paracetamol"
              value={formData.name}
              onChange={(e) =>
                setFormData({ ...formData, name: e.target.value })
              }
            />
          </div>

          <div className="grid grid-cols-2 gap-6">
            <div className="space-y-2">
              <label className="text-xs font-bold text-slate-400 uppercase tracking-widest ml-1">
                Dosage
              </label>
              <input
                type="text"
                required
                className="w-full px-6 py-4 rounded-2xl border border-slate-100 focus:ring-4 focus:ring-primary-50 focus:border-primary-300 outline-none transition-all text-slate-800 font-medium placeholder:text-slate-300"
                placeholder="500mg"
                value={formData.dosage}
                onChange={(e) =>
                  setFormData({ ...formData, dosage: e.target.value })
                }
              />
            </div>
            <div className="space-y-2">
              <label className="text-xs font-bold text-slate-400 uppercase tracking-widest ml-1">
                Condition
              </label>
              <select
                className="w-full px-6 py-4 rounded-2xl border border-slate-100 focus:ring-4 focus:ring-primary-50 focus:border-primary-300 outline-none transition-all appearance-none bg-white font-semibold text-slate-800"
                value={formData.condition}
                onChange={(e) =>
                  setFormData({ ...formData, condition: e.target.value })
                }
              >
                <option value="after food">After Food</option>
                <option value="before food">Before Food</option>
                <option value="empty stomach">Empty Stomach</option>
              </select>
            </div>
          </div>

          <div className="space-y-2">
            <label className="text-xs font-bold text-slate-400 uppercase tracking-widest ml-1">
              Reminder Time
            </label>
            <div className="relative">
              <Clock
                className="absolute left-6 top-1/2 -translate-y-1/2 text-slate-300"
                size={20}
              />
              <input
                type="time"
                required
                className="w-full pl-16 pr-6 py-4 rounded-2xl border border-slate-100 focus:ring-4 focus:ring-primary-50 focus:border-primary-300 outline-none transition-all font-semibold text-slate-800"
                value={formData.time[0]}
                onChange={(e) =>
                  setFormData({ ...formData, time: [e.target.value] })
                }
              />
            </div>
          </div>

          <div className="pt-6 flex gap-4">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-8 py-4 rounded-2xl border border-slate-100 text-slate-500 font-semibold hover:bg-slate-50 transition-all active:scale-95"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="flex-1 px-8 py-4 rounded-2xl bg-primary-600 text-white font-bold hover:bg-primary-700 shadow-xl shadow-primary-200 transition-all active:scale-95"
            >
              {medicine ? "Save Changes" : "Create Reminder"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default MedicineModal;
