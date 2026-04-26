import React from 'react';
import { Activity, Thermometer, Zap, List } from 'lucide-react';

function Dashboard({ state, onToggle, onRunScene }) {
  const devices = Object.entries(state.devices || {});
  const totalDevices = devices.length;
  const activeDevices = devices.filter(([_, d]) => d.on).length;
  const thermostat = devices.find(([_, d]) => d.type === 'thermostat')?.[1];
  const currentTemp = thermostat?.temp || '--';

  const quickDevices = ['Living Room Light', 'Kitchen Light', 'Smart TV', 'Front Door Lock'];

  return (
    <div className="dashboard-container">
      <div className="metric-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1.5rem', marginBottom: '2rem' }}>
        <div className="glass-panel" style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <div style={{ background: 'rgba(59, 130, 246, 0.2)', padding: '1rem', borderRadius: '50%', color: 'var(--accent-blue)' }}>
            <Activity size={24} />
          </div>
          <div>
            <div style={{ fontSize: '2rem', fontWeight: 'bold', fontFamily: 'Space Mono' }}>{activeDevices} / {totalDevices}</div>
            <div style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>Devices Active</div>
          </div>
        </div>

        <div className="glass-panel" style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <div style={{ background: 'rgba(245, 158, 11, 0.2)', padding: '1rem', borderRadius: '50%', color: 'var(--accent-orange)' }}>
            <Thermometer size={24} />
          </div>
          <div>
            <div style={{ fontSize: '2rem', fontWeight: 'bold', fontFamily: 'Space Mono' }}>{currentTemp}°C</div>
            <div style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>Indoor Temp</div>
          </div>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1.5rem' }}>
        <div className="glass-panel">
          <h2 className="mono-text" style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '1rem', letterSpacing: '2px', textTransform: 'uppercase' }}>Quick Toggles</h2>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
            {quickDevices.map(name => {
              const d = state.devices[name];
              if (!d) return null;
              return (
                <button 
                  key={name}
                  onClick={() => onToggle(name)}
                  style={{
                    background: d.on ? 'rgba(16, 185, 129, 0.15)' : 'rgba(255, 255, 255, 0.05)',
                    border: `1px solid ${d.on ? 'rgba(16, 185, 129, 0.3)' : 'rgba(255, 255, 255, 0.1)'}`,
                    borderRadius: '12px',
                    padding: '1rem',
                    textAlign: 'left',
                    cursor: 'pointer',
                    transition: 'all 0.2s',
                    color: 'var(--text-primary)'
                  }}
                >
                  <div style={{ fontSize: '1.5rem', marginBottom: '0.5rem' }}>{d.icon}</div>
                  <div style={{ fontSize: '0.9rem', fontWeight: 'bold' }}>{name}</div>
                  <div style={{ fontSize: '0.75rem', color: d.on ? 'var(--accent-green)' : 'var(--text-secondary)' }}>{d.on ? 'ON' : 'OFF'}</div>
                </button>
              )
            })}
          </div>
        </div>

        <div className="glass-panel" style={{ display: 'flex', flexDirection: 'column' }}>
          <h2 className="mono-text" style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '1rem', letterSpacing: '2px', textTransform: 'uppercase' }}>Quick Scenes</h2>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '1rem', marginBottom: '2rem' }}>
             {["🌅 Morning", "🎬 Movie", "😴 Sleep", "🏃 Away"].map(scene => (
              <button 
                key={scene} 
                className="btn-secondary" 
                onClick={() => onRunScene(scene)}
                style={{ flex: '1 1 45%' }}
              >
                {scene}
              </button>
            ))}
          </div>

          <h2 className="mono-text" style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '1rem', letterSpacing: '2px', textTransform: 'uppercase' }}>Recent Activity</h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', flex: 1 }}>
            {(state.action_log || []).slice(0, 3).map((log, i) => (
               <div key={i} style={{ display: 'flex', alignItems: 'center', fontSize: '0.85rem', background: 'rgba(255,255,255,0.03)', padding: '0.5rem', borderRadius: '8px' }}>
                 <span style={{ color: 'var(--text-secondary)', width: '60px' }}>{log.time}</span>
                 <span style={{ color: 'var(--text-primary)' }}>{log.action}</span>
               </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
