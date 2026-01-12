import React from 'react';
import { Activity } from 'lucide-react';

const Header = ({ user, onLogout }) => {
  return (
    <div className="bg-white border-b border-gray-200 sticky top-0 z-10 shadow-sm">
      <div className="max-w-7xl mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="w-10 h-10 bg-teal-500 rounded-xl flex items-center justify-center shadow-md">
              <Activity className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">Healthcare ERP</h1>
              <p className="text-sm text-gray-500">Nurse Dashboard</p>
            </div>
          </div>

          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-teal-100 rounded-full flex items-center justify-center">
                <span className="text-sm font-semibold text-teal-600">
                  {user?.email?.substring(0, 2).toUpperCase() || 'JD'}
                </span>
              </div>
              <span className="text-sm font-medium text-gray-700">
                {user?.email?.split('@')[0] || 'User'}
              </span>
            </div>
            <button
              onClick={onLogout}
              className="text-sm text-gray-600 hover:text-gray-900 px-3 py-2 rounded-lg hover:bg-gray-100 transition-colors"
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Header;