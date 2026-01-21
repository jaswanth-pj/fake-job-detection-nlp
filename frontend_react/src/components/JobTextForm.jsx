import { useState } from "react";
import { predictText } from "../services/api";

function JobTextForm() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [flagged, setFlagged] = useState(false);

  const handleSubmit = async () => {
    if (!text.trim()) return;

    setLoading(true);
    setError(null);
    setFlagged(false);

    try {
      const res = await predictText(text);
      setResult(res);
    } catch (err) {
      setError("Prediction failed. Please try again.");
    }

    setLoading(false);
  };

 
  const handleFlag = async () => {
    try {
      await fetch(
        `http://localhost:5000/flag/${result.prediction_id}`,
        { method: "POST" }
      );
      setFlagged(true);
    } catch (err) {
      alert("Failed to flag prediction");
    }
  };

  return (
    <div>
      <h3>Check Job Description</h3>

      <textarea
        rows="5"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Paste job description here..."
      />

      <br />

      <button onClick={handleSubmit}>
        {loading ? "Checking..." : "Check"}
      </button>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {result && (
        <div style={{ marginTop: "15px", fontWeight: "bold" }}>
          {result.label === 1 ? (
            <p>⚠️ This job posting is FAKE. Please be careful.</p>
          ) : (
            <p>✅ This job posting is REAL. Avoid sharing personal details.</p>
          )}

          <p style={{ fontSize: "14px", opacity: 0.8 }}>
            Confidence: {result.confidence}%
          </p>

          {!flagged ? (
            <button
              onClick={handleFlag}
              style={{
                marginTop: "10px",
                backgroundColor: "#ff9800",
                color: "white",
                border: "none",
                padding: "6px 12px",
                cursor: "pointer",
              }}
            >
              Flag as Suspicious
            </button>
          ) : (
            <p style={{ color: "green", marginTop: "10px" }}>
              ✅ Thanks for your feedback!
            </p>
          )}
        
        </div>
      )}
    </div>
  );
}

export default JobTextForm;
