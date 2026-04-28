import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import Layout from './components/Layout';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Analyzer from './pages/Analyzer';
import Reports from './pages/Reports';
import SOS from './pages/SOS';
import Profile from './pages/Profile';
import { AlarmProvider } from './context/AlarmContext';
import AlarmOverlay from './components/AlarmOverlay';

function App() {
  return (
    <Router>
      <AuthProvider>
        <AlarmProvider>
          <div className="min-h-screen bg-slate-50 text-slate-800 font-sans selection:bg-primary-200">
            <AlarmOverlay />
            <Routes>
              <Route path="/login" element={<Login />} />
              
              <Route element={<Layout />}>
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/analyzer" element={<Analyzer />} />
                <Route path="/reports" element={<Reports />} />
                <Route path="/sos" element={<SOS />} />
                <Route path="/profile" element={<Profile />} />
                <Route path="/" element={<Navigate to="/dashboard" replace />} />
              </Route>

              <Route path="*" element={<Navigate to="/dashboard" replace />} />
            </Routes>
          </div>
        </AlarmProvider>
      </AuthProvider>
    </Router>
  );
}

export default App;
