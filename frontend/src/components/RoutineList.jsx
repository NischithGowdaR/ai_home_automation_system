import React from 'react';

function RoutineList({ routines, onRunScene, onRefresh, apiUrl }) {

  const handleToggleRoutine = async (index) => {
    try {
      await fetch(`${apiUrl}/routine/toggle`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ index })
      });
      onRefresh();
    } catch (err) {
      console.error("Failed to toggle routine", err);
    }
  };

  return (
    <div>
      <div style={{ marginBottom: '2rem' }}>
        <h2 className="mono-text" style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '1rem', letterSpacing: '2px', textTransform: 'uppercase' }}>
          Quick Scenes
        </h2>
        <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
          {["🌅 Morning", "🎬 Movie", "😴 Sleep", "🏃 Away"].map(scene => (
            <button key={scene} className="btn-secondary" onClick={() => onRunScene(scene)}>
              {scene}
            </button>
          ))}
        </div>
      </div>

      <h2 className="mono-text" style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '1rem', letterSpacing: '2px', textTransform: 'uppercase' }}>
        Automation Routines
      </h2>
      <div className="routine-grid">
        {routines.map((r, i) => (
          <div key={i} className="routine-card">
            <div className="routine-header">
              <h3 style={{ fontSize: '1.1rem', color: 'var(--accent-purple)' }}>⚡ {r.name}</h3>
              <div style={{ fontSize: '0.8rem', color: r.active ? 'var(--accent-green)' : 'var(--text-secondary)', fontWeight: 'bold' }}>
                {r.active ? '● ACTIVE' : '○ INACTIVE'}
              </div>
            </div>
            <div style={{ fontSize: '0.85rem', color: 'var(--text-primary)', marginBottom: '0.5rem' }}>
              🕒 {r.trigger}
            </div>
            <div className="routine-actions">
              <strong>Actions:</strong><br />
              {r.actions.map((act, idx) => (
                <div key={idx}>• {act}</div>
              ))}
            </div>
            <div className="routine-footer">
              <button className="btn-secondary" onClick={() => handleToggleRoutine(i)}>
                {r.active ? 'Disable' : 'Enable'}
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default RoutineList;
