import React, { useState, useEffect } from 'react';
import { Mic, Smartphone, Zap, List } from 'lucide-react';
import DeviceCard from './components/DeviceCard';
import VoiceCommand from './components/VoiceCommand';
import ActionLog from './components/ActionLog';
import RoutineList from './components/RoutineList';
import Dashboard from './components/Dashboard';
import { LayoutDashboard } from 'lucide-react';

const API_BASE_URL = 'http://127.0.0.1:8000/api';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [state, setState] = useState({ devices: {}, action_log: [], routines: [] });

  const fetchState = async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/state`);
      const data = await res.json();
      setState(data);
    } catch (err) {
      console.error("Failed to fetch state:", err);
    }
  };

  useEffect(() => {
    fetchState();
    const interval = setInterval(fetchState, 3000); // Poll for updates
    return () => clearInterval(interval);
  }, []);

  const handleDeviceToggle = async (deviceName) => {
    try {
      await fetch(`${API_BASE_URL}/device/toggle`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ device_name: deviceName })
      });
      fetchState();
    } catch (err) {
      console.error("Toggle failed:", err);
    }
  };

  const handleDeviceSet = async (deviceName, property, value) => {
    try {
      await fetch(`${API_BASE_URL}/device/set`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ device_name: deviceName, property, value })
      });
      fetchState();
    } catch (err) {
      console.error("Set property failed:", err);
    }
  };

  const handleTextCommand = async (command) => {
    try {
      const res = await fetch(`${API_BASE_URL}/command/text`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ command })
      });
      const data = await res.json();
      fetchState();
      return data;
    } catch (err) {
      console.error("Command failed:", err);
      throw err;
    }
  };

  const handleVoiceCommand = async (audioBlob) => {
    try {
      const formData = new FormData();
      formData.append('file', audioBlob, 'command.webm');
      
      const res = await fetch(`${API_BASE_URL}/command/voice`, {
        method: 'POST',
        body: formData
      });
      const data = await res.json();
      fetchState();
      return data;
    } catch (err) {
      console.error("Voice command failed:", err);
      throw err;
    }
  };
  
  const handleRunScene = async (sceneName) => {
    try {
      await fetch(`${API_BASE_URL}/scene/run`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ scene_name: sceneName })
      });
      fetchState();
    } catch (err) {
      console.error("Run scene failed", err);
    }
  };

  return (
    <div className="app-container">
      <header className="header">
        <div>
          <h1><span className="gradient-text">SmartHome</span> AI</h1>
          <p className="header-subtitle">AI-powered home automation • Voice commands</p>
        </div>
      </header>

      <div className="tabs-container">
        <button 
          className={`tab-btn ${activeTab === 'dashboard' ? 'active' : ''}`}
          onClick={() => setActiveTab('dashboard')}
        >
          <LayoutDashboard size={18} /> Dashboard
        </button>
        <button 
          className={`tab-btn ${activeTab === 'voice' ? 'active' : ''}`}
          onClick={() => setActiveTab('voice')}
        >
          <Mic size={18} /> Voice Control
        </button>
        <button 
          className={`tab-btn ${activeTab === 'devices' ? 'active' : ''}`}
          onClick={() => setActiveTab('devices')}
        >
          <Smartphone size={18} /> Devices
        </button>
        <button 
          className={`tab-btn ${activeTab === 'routines' ? 'active' : ''}`}
          onClick={() => setActiveTab('routines')}
        >
          <Zap size={18} /> Routines
        </button>
        <button 
          className={`tab-btn ${activeTab === 'log' ? 'active' : ''}`}
          onClick={() => setActiveTab('log')}
        >
          <List size={18} /> Action Log
        </button>
      </div>

      <main>
        {activeTab === 'dashboard' && (
          <Dashboard 
            state={state} 
            onToggle={handleDeviceToggle} 
            onRunScene={handleRunScene} 
          />
        )}

        {activeTab === 'voice' && (
          <div className="glass-panel">
            <h2 className="mono-text" style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '1rem', letterSpacing: '2px', textTransform: 'uppercase' }}>
              AI Voice Command Center
            </h2>
            <VoiceCommand 
              onTextCommand={handleTextCommand} 
              onVoiceCommand={handleVoiceCommand}
            />
          </div>
        )}

        {activeTab === 'devices' && (
          <div className="device-grid">
            {Object.keys(state.devices).length === 0 ? (
              <div style={{ color: 'var(--text-secondary)' }}>Loading devices or unable to connect to backend...</div>
            ) : (
              Object.entries(state.devices).map(([name, d]) => (
                <DeviceCard 
                  key={name} 
                  name={name} 
                  device={d} 
                  onToggle={() => handleDeviceToggle(name)}
                  onSet={(prop, val) => handleDeviceSet(name, prop, val)}
                />
              ))
            )}
          </div>
        )}

        {activeTab === 'routines' && (
          <RoutineList 
            routines={state.routines} 
            onRunScene={handleRunScene}
            onRefresh={fetchState}
            apiUrl={API_BASE_URL}
          />
        )}

        {activeTab === 'log' && (
          <div className="glass-panel">
            <h2 className="mono-text" style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '1rem', letterSpacing: '2px', textTransform: 'uppercase' }}>
              System Activity
            </h2>
            <ActionLog logs={state.action_log} />
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
