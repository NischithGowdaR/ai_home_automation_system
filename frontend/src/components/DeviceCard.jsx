import React from 'react';

function DeviceCard({ name, device, onToggle, onSet }) {
  const isThermostatOrAc = device.type === 'thermostat' || device.type === 'ac';
  const isLight = device.type === 'light';
  const isFan = device.type === 'fan';

  return (
    <div className={`device-card ${device.on ? 'on' : ''}`}>
      <div className="device-header">
        <div className="device-icon-container">
          {device.icon}
        </div>
        <div style={{ textAlign: 'right' }}>
          <div style={{ color: device.on ? 'var(--accent-green)' : 'var(--text-secondary)', fontWeight: 'bold', fontSize: '0.9rem' }}>
            {device.on ? 'ON' : 'OFF'}
          </div>
          {isThermostatOrAc && <div style={{ fontSize: '0.8rem', color: 'var(--accent-orange)' }}>{device.temp}°C</div>}
          {isLight && device.on && <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>{device.brightness}%</div>}
        </div>
      </div>
      
      <div className="device-info">
        <h3 className="mono-text">{name}</h3>
        <div className="device-room">{device.room}</div>
      </div>

      <div className="device-controls">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>Power</span>
          <label className="toggle-switch">
            <input type="checkbox" checked={device.on} onChange={onToggle} />
            <span className="slider"></span>
          </label>
        </div>

        {isThermostatOrAc && device.on && (
          <div style={{ marginTop: '1rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem' }}>
              <span>Temperature</span>
              <span>{device.temp}°C</span>
            </div>
            <input 
              type="range" 
              min="16" max="30" 
              value={device.temp} 
              onChange={(e) => onSet('temp', parseInt(e.target.value))}
              className="range-slider"
            />
          </div>
        )}

        {isLight && device.on && (
          <div style={{ marginTop: '1rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem' }}>
              <span>Brightness</span>
              <span>{device.brightness}%</span>
            </div>
            <input 
              type="range" 
              min="10" max="100" 
              value={device.brightness} 
              onChange={(e) => onSet('brightness', parseInt(e.target.value))}
              className="range-slider"
            />
          </div>
        )}

        {isFan && device.on && (
          <div style={{ marginTop: '1rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem' }}>
              <span>Speed</span>
              <span>{device.speed}/3</span>
            </div>
            <input 
              type="range" 
              min="1" max="3" 
              value={device.speed} 
              onChange={(e) => onSet('speed', parseInt(e.target.value))}
              className="range-slider"
            />
          </div>
        )}
      </div>
    </div>
  );
}

export default DeviceCard;
