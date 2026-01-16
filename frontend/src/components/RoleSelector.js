import React from 'react';
import { Activity, Stethoscope, Pill } from 'lucide-react';

const RoleSelector = ({ onSelectRole }) => {
  const roles = [
    { id: 'nurse', name: 'Nurse', icon: Activity, isImage: false, description: 'Patient care & vitals monitoring' },
    { id: 'doctor', name: 'Doctor', icon: Stethoscope, isImage: false, description: 'Diagnosis & treatment' },
    { id: 'pharmacist', name: 'Pharmacist', icon: Pill, isImage: false, description: 'Medication management' },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-teal-50 to-blue-50 flex items-center justify-center p-4">
      <div className="w-full max-w-4xl">
        <div className="text-center mb-12">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-teal-500 rounded-2xl mb-6 shadow-lg overflow-hidden">
            <img src="/logo.jpg" alt="Logo" className="w-full h-full object-cover" />
          </div>
          <h1 className="text-4xl font-bold text-gray-900 mb-3">Healthcare ERP</h1>
          <p className="text-gray-600 text-lg">Select your role to continue</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {roles.map((role) => {
            const Icon = role.icon;
            return (
              <button
                key={role.id}
                onClick={() => onSelectRole(role)}
                className="bg-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-1 group"
              >
                <div className="flex flex-col items-center text-center">
                  <div className="w-20 h-20 bg-teal-100 rounded-2xl flex items-center justify-center mb-4 group-hover:bg-teal-500 transition-colors overflow-hidden">
                    {role.isImage ? (
                      <img src={role.icon} alt={role.name} className="w-full h-full object-cover" />
                    ) : (
                      <Icon className="w-10 h-10 text-teal-600 group-hover:text-white transition-colors" />
                    )}
                  </div>
                  <h3 className="text-xl font-bold text-gray-900 mb-2">{role.name}</h3>
                  <p className="text-gray-600 text-sm">{role.description}</p>
                </div>
              </button>
            );
          })}
        </div>

        <p className="text-center text-gray-500 text-sm mt-12">
          Healthcare Management System v1.0
        </p>
      </div>
    </div>
  );
};

export default RoleSelector;