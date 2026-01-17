import React from 'react';
import { Activity, Stethoscope, Pill, Lock } from 'lucide-react';

const RoleSelector = ({ onSelectRole }) => {
  const roles = [
    { 
      id: 'nurse', 
      name: 'Nurse', 
      icon: Activity, 
      description: 'Patient care & vitals monitoring',
      disabled: false // ✅ Active
    },
    { 
      id: 'doctor', 
      name: 'Doctor', 
      icon: Stethoscope, 
      description: 'Diagnosis & treatment',
      disabled: true // 🔒 Locked
    },
    { 
      id: 'pharmacist', 
      name: 'Pharmacist', 
      icon: Pill, 
      description: 'Medication management',
      disabled: true // 🔒 Locked
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-teal-50 to-blue-50 flex items-center justify-center p-4">
      <div className="w-full max-w-4xl">
        <div className="text-center mb-12">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-teal-500 rounded-2xl mb-6 shadow-lg">
            <Activity className="w-10 h-10 text-white" />
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
                disabled={role.disabled}
                onClick={() => !role.disabled && onSelectRole(role)}
                // ✅ All cards get hover effects (shadow, translate)
                className={`relative rounded-2xl p-8 transition-all duration-300 group bg-white shadow-lg 
                  hover:shadow-xl hover:-translate-y-1
                  ${role.disabled ? 'cursor-not-allowed' : 'cursor-pointer'}
                `}
              >
                {/* Lock icon overlay for disabled roles */}
                {role.disabled && (
                  <div className="absolute top-4 right-4 bg-gray-100 p-1.5 rounded-full z-10">
                    <Lock className="w-5 h-5 text-gray-500" />
                  </div>
                )}

                <div className="flex flex-col items-center text-center">
                  {/* ✅ Icon Container - All cards get hover color change */}
                  <div className="w-20 h-20 rounded-2xl flex items-center justify-center mb-4 transition-colors 
                    bg-teal-100 group-hover:bg-teal-500">
                    
                    {/* ✅ Icon - All cards get hover color change */}
                    <Icon className="w-10 h-10 transition-colors text-teal-600 group-hover:text-white" />
                  </div>
                  
                  <h3 className="text-xl font-bold text-gray-900 mb-2">
                    {role.name}
                  </h3>
                  <p className="text-gray-600 text-sm">
                    {role.disabled ? 'Access Restricted' : role.description}
                  </p>
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