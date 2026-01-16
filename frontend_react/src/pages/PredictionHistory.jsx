import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getPredictionHistory } from "../services/api";
import "../styles/history.css";

function PredictionHistory() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    getPredictionHistory()
      .then((data) => {
        setHistory(data);
        setLoading(false);
      })
      .catch(() => {
        alert("Failed to load history");
        setLoading(false);
      });
  }, []);

  /* 🔽 DOWNLOAD HISTORY FUNCTION */
  const downloadHistory = () => {
    if (history.length === 0) {
      alert("No history to download");
      return;
    }

    // CSV header
    let csv = "Result,Date,Text\n";

    history.forEach((item) => {
      const text = `"${item.text.replace(/"/g, '""')}"`;
      csv += `${item.result},${item.created_at},${text}\n`;
    });

    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");
    link.href = url;
    link.download = "prediction_history.csv";
    link.click();

    URL.revokeObjectURL(url);
  };

  if (loading) {
    return <p>Loading history...</p>;
  }

  return (
    <div className="history-container">
      {/* TOP ACTIONS */}
      <div className="history-actions">
        <button
          className="history-back-btn"
          onClick={() => navigate("/detect")}
        >
          Back to Detection
        </button>

        <button
          className="history-download-btn"
          onClick={downloadHistory}
        >
          Download History
        </button>
      </div>

      <h2 className="history-title">Prediction History</h2>

      {history.length === 0 && (
        <p className="history-empty">No predictions yet.</p>
      )}

      <div className="history-list">
        {history.map((item, index) => (
          <div className="history-card" key={index}>
            <div className="history-top">
              <span
                className={`history-tag ${
                  item.result === "Fake Job" ? "fake" : "real"
                }`}
              >
                {item.result}
              </span>

              <span className="history-date">
                {item.created_at}
              </span>
            </div>

            <div className="history-text">
              {item.text}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default PredictionHistory;
