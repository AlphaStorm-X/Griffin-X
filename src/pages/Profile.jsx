import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { User, Mail, Save, FileText } from 'lucide-react';

const Profile = () => {
  const { user, updateProfile } = useAuth();
  const [formData, setFormData] = useState({
    name: user?.name || '',
    email: user?.email || '',
    bloodType: user?.bloodType || 'Not specified',
    allergies: user?.allergies || 'None',
  });
  const [isEditing, setIsEditing] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSave = () => {
    updateProfile({ ...formData });
    setIsEditing(false);
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-500 max-w-3xl mx-auto pb-10">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-slate-800">My Profile</h1>
          <p className="text-slate-500 mt-2">Manage your personal and medical details.</p>
        </div>
        {isEditing ? (
          <button 
            onClick={handleSave}
            className="px-4 py-2 bg-primary-500 hover:bg-primary-600 text-white rounded-xl font-medium shadow-md transition-colors flex items-center gap-2"
          >
            <Save size={18} /> Save Changes
          </button>
        ) : (
          <button 
            onClick={() => setIsEditing(true)}
            className="px-4 py-2 bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 hover:text-primary-600 rounded-xl font-medium shadow-sm transition-colors flex items-center gap-2"
          >
            Edit Profile
          </button>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="md:col-span-1 space-y-6">
          <div className="glass-card p-6 flex flex-col items-center text-center">
             <div className="w-24 h-24 rounded-2xl bg-gradient-to-br from-primary-400 to-primary-600 flex items-center justify-center text-white font-bold text-4xl shadow-lg mb-4">
              {user?.name?.charAt(0) || 'A'}
            </div>
            <h2 className="text-xl font-bold text-slate-800">{user?.name}</h2>
            <p className="text-slate-500 text-sm mt-1">{formData.bloodType} Blood Type</p>
            
            <div className="mt-6 w-full pt-6 border-t border-slate-100 flex justify-between text-sm">
              <div className="text-center">
                <span className="block font-bold text-slate-800">3</span>
                <span className="text-slate-500">Meds</span>
              </div>
              <div className="text-center border-l border-slate-100 pl-4">
                <span className="block font-bold text-slate-800">5</span>
                <span className="text-slate-500">Reports</span>
              </div>
            </div>
          </div>
        </div>

        <div className="md:col-span-2 space-y-6">
          <div className="glass-card p-6 space-y-6">
            <h3 className="text-lg font-bold text-slate-800 border-b border-slate-100 pb-2 mb-4">Personal Information</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-1">
                <label className="text-sm font-medium text-slate-500 flex items-center gap-1">
                  <User size={14} /> Full Name
                </label>
                {isEditing ? (
                  <input
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    className="w-full px-3 py-2 rounded-lg border border-slate-200 bg-white focus:border-primary-400 focus:ring-1 focus:ring-primary-100 outline-none"
                  />
                ) : (
                  <p className="text-slate-800 font-medium py-2">{formData.name}</p>
                )}
              </div>

              <div className="space-y-1">
                <label className="text-sm font-medium text-slate-500 flex items-center gap-1">
                  <Mail size={14} /> Email Address
                </label>
                {isEditing ? (
                  <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    className="w-full px-3 py-2 rounded-lg border border-slate-200 bg-white focus:border-primary-400 focus:ring-1 focus:ring-primary-100 outline-none"
                  />
                ) : (
                  <p className="text-slate-800 font-medium py-2">{formData.email}</p>
                )}
              </div>
            </div>

            <h3 className="text-lg font-bold text-slate-800 border-b border-slate-100 pb-2 mt-8 mb-4">Medical Details</h3>

             <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-1">
                <label className="text-sm font-medium text-slate-500 flex items-center gap-1">
                  Blood Type
                </label>
                {isEditing ? (
                  <select
                    name="bloodType"
                    value={formData.bloodType}
                    onChange={handleChange}
                    className="w-full px-3 py-2 rounded-lg border border-slate-200 bg-white focus:border-primary-400 focus:ring-1 focus:ring-primary-100 outline-none"
                  >
                    <option>Not specified</option>
                    <option>A+</option><option>A-</option>
                    <option>B+</option><option>B-</option>
                    <option>AB+</option><option>AB-</option>
                    <option>O+</option><option>O-</option>
                  </select>
                ) : (
                  <p className="text-slate-800 font-medium py-2">{formData.bloodType}</p>
                )}
              </div>

              <div className="space-y-1">
                <label className="text-sm font-medium text-slate-500 flex items-center gap-1">
                 Allergies
                </label>
                {isEditing ? (
                  <input
                    type="text"
                    name="allergies"
                    value={formData.allergies}
                    onChange={handleChange}
                    className="w-full px-3 py-2 rounded-lg border border-slate-200 bg-white focus:border-primary-400 focus:ring-1 focus:ring-primary-100 outline-none"
                  />
                ) : (
                  <p className="text-slate-800 font-medium py-2">{formData.allergies}</p>
                )}
              </div>
            </div>
            
            <div className="p-4 bg-blue-50/50 rounded-xl border border-blue-100 mt-6 flex gap-3">
              <FileText className="text-blue-500 shrink-0" size={20} />
              <div>
                <p className="text-sm font-medium text-blue-900">Your data is stored locally</p>
                <p className="text-xs text-blue-700 mt-1">AuraCare prioritizes your privacy. Your profile and medical details are stored securely on your device using localStorage.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;
