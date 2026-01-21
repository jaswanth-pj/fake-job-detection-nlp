import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Pie } from "react-chartjs-2";
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend
} from "chart.js";
import "../styles/userDashboard.css";

ChartJS.register(ArcElement, Tooltip, Legend);

function UserDashboard() {
  const [data, setData] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const userId = localStorage.getItem("userId");
    if (!userId) {
      navigate("/login");
      return;
    }

    fetch(`http://127.0.0.1:5000/user/dashboard/${userId}`)
      .then(res => res.json())
      .then(data => setData(data));
  }, [navigate]);

  if (!data) return <p>Loading...</p>;

  const pieData = {
    labels: ["Real Jobs", "Fake Jobs"],
    datasets: [
      {
        data: [data.real, data.fake],
        backgroundColor: ["#22c55e", "#ef4444"],
        borderWidth: 0,
      },
    ],
  };

  return (
    <div className="user-dashboard">
      
      <div className="user-header">
        <h2>User Dashboard</h2>
        <button  className="dash-back-btn"onClick={() => navigate("/detect")}>
          ← Back to Detection
        </button>
      </div>

    
      <div className="stats-grid">
        <div className="stat-card">
          <p>Total Detections</p>
          <h3 className="stat-total">{data.total_predictions}</h3>
        </div>

        <div className="stat-card">
          <p>Fake Jobs</p>
          <h3 className="stat-fake">{data.fake}</h3>
        </div>

        <div className="stat-card">
          <p>Real Jobs</p>
          <h3 className="stat-real">{data.real}</h3>
        </div>
      </div>

     
      <div className="chart-section">
        <div className="chart-card">
          <div className="chart-title">
            Fake vs Real Job Distribution
          </div>
          <Pie data={pieData} />
        </div>

        <div className="chart-card">
          <div className="chart-title">
            Insights
          </div>
          <ul style={{ lineHeight: "1.9", fontSize: "14px" }}>
            <li>✔ Helps users understand detection trends</li>
            <li>✔ Visual confidence in model output</li>
            <li>✔ Encourages safer job searching</li>
            <li>✔ Improves decision-making</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default UserDashboard;
