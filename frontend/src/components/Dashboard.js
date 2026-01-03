import React, { useState } from 'react';
import { UserPlus } from 'lucide-react';
import Header from './Header';

const Dashboard = ({ user, onLogout }) => {
  const [searchQuery, setSearchQuery] = useState('');

  const mockPatients = [
    { id: 'P001', name: 'John Doe', age: 45, gender: 'Male', lastVisit: '2024-12-20', status: 'stable' },
    { id: 'P002', name: 'Jane Smith', age: 62, gender: 'Female', lastVisit: '2024-12-22', status: 'monitoring' },
    { id: 'P003', name: 'Robert Johnson', age: 38, gender: 'Male', lastVisit: '2024-12-23', status: 'stable' },
    { id: 'P004', name: 'Maria Garcia', age: 55, gender: 'Female', lastVisit: '2024-12-24', status: 'alert' },
  ];

  const filteredPatients = mockPatients.filter(p => 
    p.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
    p.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const statusColors = {
    stable: 'bg-green-100 text-green-700',
    monitoring: 'bg-yellow-100 text-yellow-700',
    alert: 'bg-red-100 text-red-700',
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header user={user} onLogout={onLogout} />

      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Search & Actions */}
        <div className="flex items-center justify-between mb-6 gap-4">
          <div className="flex-1 max-w-2xl relative">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search by Patient ID or Name..."
              className="w-full px-4 py-3 pl-11 border border-gray-300 rounded-xl focus:ring-2 focus:ring-teal-500 focus:border-transparent shadow-sm"
            />
            <svg className="w-5 h-5 text-gray-400 absolute left-4 top-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
          
          <button className="flex items-center space-x-2 bg-teal-500 text-white px-6 py-3 rounded-xl hover:bg-teal-600 transition-colors font-medium shadow-lg">
            <UserPlus className="w-5 h-5" />
            <span>New Patient</span>
          </button>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <div className="bg-white rounded-xl p-4 border border-gray-200 shadow-sm">
            <p className="text-gray-600 text-sm mb-1">Total Patients</p>
            <p className="text-2xl font-bold text-gray-900">{mockPatients.length}</p>
          </div>
          <div className="bg-green-50 rounded-xl p-4 border border-green-200 shadow-sm">
            <p className="text-green-700 text-sm mb-1">Stable</p>
            <p className="text-2xl font-bold text-green-900">2</p>
          </div>
          <div className="bg-yellow-50 rounded-xl p-4 border border-yellow-200 shadow-sm">
            <p className="text-yellow-700 text-sm mb-1">Monitoring</p>
            <p className="text-2xl font-bold text-yellow-900">1</p>
          </div>
          <div className="bg-red-50 rounded-xl p-4 border border-red-200 shadow-sm">
            <p className="text-red-700 text-sm mb-1">Alerts</p>
            <p className="text-2xl font-bold text-red-900">1</p>
          </div>
        </div>

        {/* Patient List */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-200 bg-gray-50">
            <h2 className="text-lg font-semibold text-gray-900">
              {searchQuery ? `Search Results (${filteredPatients.length})` : 'All Patients'}
            </h2>
          </div>

          <div className="divide-y divide-gray-200">
            {filteredPatients.map((patient) => (
              <div
                key={patient.id}
                className="px-6 py-4 hover:bg-teal-50 cursor-pointer transition-colors"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-4">
                    <div className="w-12 h-12 bg-gradient-to-br from-teal-400 to-teal-600 rounded-xl flex items-center justify-center shadow-md">
                      <span className="text-lg font-bold text-white">
                        {patient.name.split(' ').map(n => n[0]).join('')}
                      </span>
                    </div>
                    <div>
                      <h3 className="text-base font-semibold text-gray-900">{patient.name}</h3>
                      <p className="text-sm text-gray-500">
                        {patient.id} • {patient.age}y • {patient.gender}
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center space-x-4">
                    <div className="text-right">
                      <p className="text-sm text-gray-500">Last Visit</p>
                      <p className="text-sm font-medium text-gray-900">{patient.lastVisit}</p>
                    </div>
                    <span className={`px-3 py-1 rounded-full text-xs font-medium ${statusColors[patient.status]}`}>
                      {patient.status.charAt(0).toUpperCase() + patient.status.slice(1)}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;