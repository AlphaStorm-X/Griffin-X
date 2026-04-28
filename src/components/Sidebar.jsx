import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { LayoutDashboard, ScanSearch, FileText, AlertTriangle, User, LogOut } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

const Sidebar = () => {
  const { logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const navItems = [
    { name: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
    { name: 'Medicine Analyzer', path: '/analyzer', icon: ScanSearch },
    { name: 'Reports', path: '/reports', icon: FileText },
    { name: 'SOS', path: '/sos', icon: AlertTriangle, color: 'text-red-500' },
    { name: 'Profile', path: '/profile', icon: User },
  ];

  return (
    <aside className="w-64 glass shadow-lg border-r border-white/40 h-screen fixed top-0 left-0 flex flex-col transition-all duration-300 z-50">
      <div className="p-6 flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-400 to-primary-600 flex items-center justify-center text-white font-bold text-xl shadow-md">
          A
        </div>
        <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary-600 to-blue-400">
          AuraCare
        </span>
      </div>

      <nav className="flex-1 mt-6 px-4 space-y-2">
        {navItems.map((item) => (
          <NavLink
            key={item.name}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 ${
                isActive
                  ? 'bg-primary-50 text-primary-600 shadow-sm border border-primary-100'
                  : 'text-slate-500 hover:bg-white/50 hover:text-primary-500'
              }`
            }
          >
            <item.icon size={20} className={item.color || ''} />
            <span className="font-medium">{item.name}</span>
          </NavLink>
        ))}
      </nav>

      <div className="p-4 border-t border-slate-200/50">
        <button
          onClick={handleLogout}
          className="flex w-full items-center gap-3 px-4 py-3 text-slate-500 hover:bg-white/50 hover:text-red-500 rounded-xl transition-all duration-200"
        >
          <LogOut size={20} />
          <span className="font-medium">Logout</span>
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;
