import { useState } from "react";
import { predictImage } from "../services/api";

function JobImageForm() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  const handleSubmit = async () => {
    if (!file) return;
    const res = await predictImage(file);
    setResult(res);
  };

  return (
    <div>
      <h3>Check Job Poster Image</h3>

      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <br />
      <button onClick={handleSubmit}>Upload & Check</button>

      
     {result && (
  <p style={{ marginTop: "15px", fontWeight: "bold" }}>
    {result.label  === 1
      ? "⚠️ This job posting is FAKE. Please be careful."
      : "✅ This job posting is REAL."}
       
      
  </p>
)}
    </div>
  );
}

export default JobImageForm;
