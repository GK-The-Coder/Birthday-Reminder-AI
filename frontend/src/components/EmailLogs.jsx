function normalizeStatus(status) {
  if (!status) return 'unknown';
  return status.toString().trim().toLowerCase().replace(/\s+/g, '-');
}

function EmailLogs({ logs }) {
  return (
    <div className="logs-container">
      <h2>Email History</h2>

      {logs.length > 0 ? (
        logs.map((log) => {
          const statusKey = normalizeStatus(log.status);
          const statusClass = `status-badge status-badge--${statusKey}`;

          return (
            <div key={log._id} className="log-card">
              <div className="log-card__row">
                <div>
                  <h4>{log.name}</h4>
                  <p>{log.email}</p>
                </div>
                <span className={statusClass}>{log.status || 'Unknown'}</span>
              </div>
              {log.message && <p className="log-note">{log.message}</p>}
            </div>
          );
        })
      ) : (
        <p>No emails sent yet</p>
      )}
    </div>
  );
}

export default EmailLogs;
