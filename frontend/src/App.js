import React, { useState } from 'react';
import RoleSelector from './components/RoleSelector';
import Login from './components/Login';
import Dashboard from './components/Dashboard';

function App() {
  const [currentView, setCurrentView] = useState('roleSelector');
  const [selectedRole, setSelectedRole] = useState(null);
  const [user, setUser] = useState(null);

  const handleRoleSelect = (role) => {
    setSelectedRole(role);
    setCurrentView('login');
  };

  const handleLogin = (credentials) => {
    setUser({ ...credentials, role: selectedRole.id });
    setCurrentView('dashboard');
  };

  const handleLogout = () => {
    setUser(null);
    setSelectedRole(null);
    setCurrentView('roleSelector');
  };

  const handleBackToRoles = () => {
    setSelectedRole(null);
    setCurrentView('roleSelector');
  };

  return (
    <div className="App">
      {currentView === 'roleSelector' && (
        <RoleSelector onSelectRole={handleRoleSelect} />
      )}
      
      {currentView === 'login' && (
        <Login 
          selectedRole={selectedRole}
          onLogin={handleLogin}
          onBack={handleBackToRoles}
        />
      )}
      
      {currentView === 'dashboard' && (
        <Dashboard 
          user={user}
          onLogout={handleLogout}
        />
      )}
    </div>
  );
}

export default App;