import React from 'react';

function ActionLog({ logs }) {
  if (!logs || logs.length === 0) {
    return <div style={{ color: 'var(--text-secondary)', textAlign: 'center', padding: '2rem' }}>No actions logged yet.</div>;
  }

  return (
    <div className="log-list">
      {logs.map((log, i) => (
        <div key={i} className="log-entry">
          <div className="log-time mono-text">{log.time}</div>
          <div className={`log-badge badge-${log.type}`}>
            {log.type}
          </div>
          <div style={{ color: 'var(--text-primary)' }}>{log.action}</div>
        </div>
      ))}
    </div>
  );
}

export default ActionLog;
