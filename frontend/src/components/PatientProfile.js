import React, { useState, useEffect } from 'react';
import { ArrowLeft, Activity } from 'lucide-react';

const PatientProfile = ({ patient, onBack, user }) => {
  const [activeTab, setActiveTab] = useState('vitals');
  const [vitalsHistory, setVitalsHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showVitalsForm, setShowVitalsForm] = useState(false);
  const [vitalsData, setVitalsData] = useState({
    blood_pressure_systolic: '',
    blood_pressure_diastolic: '',
    heart_rate: '',
    temperature: '',
    respiratory_rate: '',
    oxygen_saturation: '',
    weight: '',
    notes: ''
  });
  const [submitResult, setSubmitResult] = useState(null);

  // Fetch patient's vitals history
  useEffect(() => {
    fetchVitalsHistory();
  }, [patient.id]);

  const fetchVitalsHistory = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/vitals/patient/${patient.id}`);
      if (response.ok) {
        const data = await response.json();
        setVitalsHistory(data);
      }
    } catch (error) {
      console.error('Error fetching vitals:', error);
    }
  };

  const handleVitalsSubmit = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/vitals/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          patient_id: patient.id,
          recorded_by_email: user.email,
          blood_pressure_systolic: parseInt(vitalsData.blood_pressure_systolic),
          blood_pressure_diastolic: parseInt(vitalsData.blood_pressure_diastolic),
          heart_rate: parseInt(vitalsData.heart_rate),
          temperature: parseFloat(vitalsData.temperature),
          respiratory_rate: parseInt(vitalsData.respiratory_rate),
          oxygen_saturation: parseInt(vitalsData.oxygen_saturation),
          weight: vitalsData.weight ? parseFloat(vitalsData.weight) : null,
          notes: vitalsData.notes
        })
      });

      if (response.ok) {
        const result = await response.json();
        setSubmitResult(result);
        setShowVitalsForm(false);
        fetchVitalsHistory(); // Refresh history
        // Clear form
        setVitalsData({
          blood_pressure_systolic: '',
          blood_pressure_diastolic: '',
          heart_rate: '',
          temperature: '',
          respiratory_rate: '',
          oxygen_saturation: '',
          weight: '',
          notes: ''
        });
      } else {
        alert('Error submitting vitals');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Error submitting vitals');
    } finally {
      setLoading(false);
    }
  };

  const getAlertColor = (level) => {
    const colors = {
      low: 'bg-green-100 border-green-500 text-green-900',
      medium: 'bg-yellow-100 border-yellow-500 text-yellow-900',
      high: 'bg-red-100 border-red-500 text-red-900',
    };
    return colors[level] || colors.low;
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 sticky top-0 z-10 shadow-sm">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <button 
                onClick={onBack}
                className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
              >
                <ArrowLeft className="w-5 h-5 text-gray-600" />
              </button>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">{patient.full_name}</h1>
                <p className="text-sm text-gray-500">
                  {patient.hospital_number} • {patient.age}y • {patient.gender}
                </p>
              </div>
            </div>
            <div className={`px-4 py-2 rounded-full text-sm font-medium ${
              patient.status === 'stable' ? 'bg-green-100 text-green-700' :
              patient.status === 'monitoring' ? 'bg-yellow-100 text-yellow-700' :
              'bg-red-100 text-red-700'
            }`}>
              {patient.status.charAt(0).toUpperCase() + patient.status.slice(1)}
            </div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-6">
          <div className="flex space-x-8">
            {['General Info', 'Vitals', 'History', 'Prescriptions'].map((tab) => {
              const tabId = tab.toLowerCase().replace(' ', '-');
              const isActive = activeTab === tabId;
              return (
                <button
                  key={tab}
                  onClick={() => setActiveTab(tabId)}
                  className={`py-4 px-2 border-b-2 font-medium text-sm transition-colors ${
                    isActive 
                      ? 'border-teal-500 text-teal-600' 
                      : 'border-transparent text-gray-500 hover:text-gray-700'
                  }`}
                >
                  {tab}
                </button>
              );
            })}
          </div>
        </div>
      </div>

      {/* Tab Content */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        
        {/* General Info Tab */}
        {activeTab === 'general-info' && (
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Patient Information</h2>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-sm text-gray-500">Hospital Number</p>
                <p className="font-medium">{patient.hospital_number}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Age</p>
                <p className="font-medium">{patient.age} years</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Gender</p>
                <p className="font-medium">{patient.gender}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Last Visit</p>
                <p className="font-medium">{patient.last_visit}</p>
              </div>
            </div>
          </div>
        )}

        {/* Vitals Tab */}
        {activeTab === 'vitals' && (
          <div className="space-y-6">
            
            {/* Submit Result Alert */}
            {submitResult && (
              <div className={`rounded-xl border-l-4 p-6 ${getAlertColor(submitResult.alert_level)}`}>
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h3 className="font-bold text-lg mb-2">
                      Vitals Recorded Successfully
                    </h3>
                    <div className="space-y-2">
                      <p className="font-medium">
                        NEWS2 Score: {submitResult.news2_score} 
                        {submitResult.alert_level === 'high' && ' - HIGH RISK'}
                        {submitResult.alert_level === 'medium' && ' - MEDIUM RISK'}
                        {submitResult.alert_level === 'low' && ' - LOW RISK'}
                      </p>
                      {submitResult.ai_interpretation && (
                        <div className="mt-4 text-sm whitespace-pre-line">
                          {submitResult.ai_interpretation}
                        </div>
                      )}
                    </div>
                  </div>
                  <button 
                    onClick={() => setSubmitResult(null)}
                    className="text-gray-500 hover:text-gray-700"
                  >
                    ✕
                  </button>
                </div>
              </div>
            )}

            {/* Record New Vitals Button/Form */}
            {!showVitalsForm ? (
              <button
                onClick={() => setShowVitalsForm(true)}
                className="w-full bg-teal-500 text-white py-4 rounded-xl font-medium hover:bg-teal-600 transition-colors shadow-lg flex items-center justify-center space-x-2"
              >
                <Activity className="w-5 h-5" />
                <span>Record New Vitals</span>
              </button>
            ) : (
              <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-6">Enter Vital Signs</h3>
                
                <div className="grid grid-cols-2 gap-6">
                  {/* Blood Pressure */}
                  <div className="col-span-2">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Blood Pressure (mmHg)
                    </label>
                    <div className="flex items-center space-x-2">
                      <input
                        type="number"
                        placeholder="Systolic"
                        value={vitalsData.blood_pressure_systolic}
                        onChange={(e) => setVitalsData({...vitalsData, blood_pressure_systolic: e.target.value})}
                        className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent"
                      />
                      <span className="text-gray-500 font-bold">/</span>
                      <input
                        type="number"
                        placeholder="Diastolic"
                        value={vitalsData.blood_pressure_diastolic}
                        onChange={(e) => setVitalsData({...vitalsData, blood_pressure_diastolic: e.target.value})}
                        className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent"
                      />
                    </div>
                  </div>

                  {/* Heart Rate */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Heart Rate (bpm)
                    </label>
                    <input
                      type="number"
                      value={vitalsData.heart_rate}
                      onChange={(e) => setVitalsData({...vitalsData, heart_rate: e.target.value})}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent"
                    />
                  </div>

                  {/* Temperature */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Temperature (°C)
                    </label>
                    <input
                      type="number"
                      step="0.1"
                      value={vitalsData.temperature}
                      onChange={(e) => setVitalsData({...vitalsData, temperature: e.target.value})}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent"
                    />
                  </div>

                  {/* Respiratory Rate */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Respiratory Rate (breaths/min)
                    </label>
                    <input
                      type="number"
                      value={vitalsData.respiratory_rate}
                      onChange={(e) => setVitalsData({...vitalsData, respiratory_rate: e.target.value})}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent"
                    />
                  </div>

                  {/* Oxygen Saturation */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Oxygen Saturation (%)
                    </label>
                    <input
                      type="number"
                      value={vitalsData.oxygen_saturation}
                      onChange={(e) => setVitalsData({...vitalsData, oxygen_saturation: e.target.value})}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent"
                    />
                  </div>

                  {/* Weight (Optional) */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Weight (kg) - Optional
                    </label>
                    <input
                      type="number"
                      step="0.1"
                      value={vitalsData.weight}
                      onChange={(e) => setVitalsData({...vitalsData, weight: e.target.value})}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent"
                    />
                  </div>

                  {/* Notes */}
                  <div className="col-span-2">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Notes
                    </label>
                    <textarea
                      value={vitalsData.notes}
                      onChange={(e) => setVitalsData({...vitalsData, notes: e.target.value})}
                      rows="3"
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent"
                      placeholder="Any additional observations..."
                    />
                  </div>
                </div>

                {/* Buttons */}
                <div className="flex space-x-4 mt-6">
                  <button
                    onClick={handleVitalsSubmit}
                    disabled={loading}
                    className="flex-1 bg-teal-500 text-white py-3 rounded-lg font-medium hover:bg-teal-600 transition-colors disabled:opacity-50"
                  >
                    {loading ? 'Submitting...' : 'Submit Vitals'}
                  </button>
                  <button
                    onClick={() => setShowVitalsForm(false)}
                    className="flex-1 bg-gray-200 text-gray-700 py-3 rounded-lg font-medium hover:bg-gray-300 transition-colors"
                  >
                    Cancel
                  </button>
                </div>
              </div>
            )}

            {/* Vitals History */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Vitals History</h3>
              {vitalsHistory.length > 0 ? (
                <div className="space-y-4">
                  {vitalsHistory.map((vital) => (
                    <div key={vital.id} className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50">
                      <div className="flex justify-between items-start mb-3">
                        <div>
                          <p className="text-sm text-gray-500">
                            {new Date(vital.recorded_at).toLocaleString()}
                          </p>
                          <p className="text-xs text-gray-400">By: {vital.recorded_by_email}</p>
                        </div>
                        <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                          vital.alert_level === 'high' ? 'bg-red-100 text-red-700' :
                          vital.alert_level === 'medium' ? 'bg-yellow-100 text-yellow-700' :
                          'bg-green-100 text-green-700'
                        }`}>
                          NEWS2: {vital.news2_score}
                        </span>
                      </div>
                      <div className="grid grid-cols-3 gap-4 text-sm">
                        <div>
                          <span className="text-gray-500">BP:</span> {vital.blood_pressure_systolic}/{vital.blood_pressure_diastolic}
                        </div>
                        <div>
                          <span className="text-gray-500">HR:</span> {vital.heart_rate} bpm
                        </div>
                        <div>
                          <span className="text-gray-500">Temp:</span> {vital.temperature}°C
                        </div>
                        <div>
                          <span className="text-gray-500">RR:</span> {vital.respiratory_rate}
                        </div>
                        <div>
                          <span className="text-gray-500">SpO2:</span> {vital.oxygen_saturation}%
                        </div>
                      </div>
                      {vital.notes && (
                        <p className="text-sm text-gray-600 mt-2">Notes: {vital.notes}</p>
                      )}
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-gray-500 text-center py-8">No vitals recorded yet</p>
              )}
            </div>
          </div>
        )}

        {/* Other tabs - placeholder */}
        {activeTab === 'history' && (
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <p className="text-gray-500">Patient history coming soon...</p>
          </div>
        )}

        {activeTab === 'prescriptions' && (
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <p className="text-gray-500">Prescriptions coming soon...</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default PatientProfile;