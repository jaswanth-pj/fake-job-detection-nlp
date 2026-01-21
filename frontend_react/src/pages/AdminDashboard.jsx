import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/adminDashboard.css";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";


function AdminDashboard() {
  const [data, setData] = useState(null);
  const [flaggedPosts, setFlaggedPosts] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const role = localStorage.getItem("role");
    if (role !== "admin") {
      navigate("/detect");
      return;
    }

    fetch("http://127.0.0.1:5000/admin/dashboard")
      .then(res => res.json())
      .then(data => setData(data))
      .catch(() => alert("Failed to load admin dashboard"));
  }, [navigate]);

  const loadFlaggedPosts = async () => {
    const res = await fetch("http://127.0.0.1:5000/admin/flagged");
    const data = await res.json();
    setFlaggedPosts(data);
  };
  const changeRole = async (userId, role) => {
  try {
    await fetch("http://127.0.0.1:5000/admin/change-role", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_id: userId,
        role: role
      })
    });

    alert("Role updated. User must login again.");

    
    const res = await fetch("http://127.0.0.1:5000/admin/dashboard");
    const updated = await res.json();
    setData(updated);

  } catch {
    alert("Failed to update role");
  }
};

  const exportCSV = () => {
    window.open("http://127.0.0.1:5000/admin/export");
  };

  const handleLogout = () => {
    localStorage.clear();
    navigate("/login");
  };

  if (!data) return <p>Loading...</p>;

  const fakeRate = ((data.fake_detected / data.total_predictions) * 100).toFixed(1);
  const realRate = (100 - fakeRate).toFixed(1);
  const chartData = [
  { name: "Fake", count: data.fake_detected },
  { name: "Real", count: data.real_detected }
];


   

  return (
    <div className="admin-container">

      {/* HEADER */}
      <div className="admin-header">
        <h2>Admin Dashboard</h2>
        <div className="admin-actions">
          <button onClick={() => navigate("/detect")}>Prediction Page</button>
          <button onClick={loadFlaggedPosts}>Flagged Posts</button>
          <button
  onClick={() =>
    window.open("http://127.0.0.1:5000/admin/export-csv", "_blank")
  }
>
  Export CSV
</button>
          <button onClick={handleLogout}>Logout</button>
        </div>
      </div>
      <h3 style={{ marginTop: "30px" }}>Prediction Distribution</h3>




      {/* STATS */}
      <div className="stats-grid">
        <div className="stat-card">Total Users <h3>{data.total_users}</h3></div>
        <div className="stat-card">Admins <h3>{data.total_admins}</h3></div>
        <div className="stat-card">Predictions <h3>{data.total_predictions}</h3></div>
        <div className="stat-card">Fake <h3>{data.fake_detected}</h3></div>
        <div className="stat-card">Real <h3>{data.real_detected}</h3></div>
        <div className="stat-card">Fake Rate <h3>{fakeRate}%</h3></div>
        <div className="stat-card">Real Rate <h3>{realRate}%</h3></div>
      </div>
<h3 style={{ marginTop: "30px" }}>Prediction Distribution</h3>



      {/* USERS TABLE */}
      <h3>Users (Last Login)</h3>
      <table className="admin-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Email</th>
            <th>Last Login</th>
            <th>Role</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {data.users.map(u => (
            <tr key={u.id}>
              <td>{u.id}</td>
              <td>{u.email}</td>
              <td>{u.last_login || "-"}</td>
              <td className={u.role === "admin" ? "role-admin" : "role-user"}>
                {u.role.toUpperCase()}
              </td>
                <td>
  {u.role === "admin" ? (
    <button
      className="btn-demote"
      onClick={() => changeRole(u.id, "user")}
    >
      Demote
    </button>
  ) : (
    <button
      className="btn-promote"
      onClick={() => changeRole(u.id, "admin")}
    >
      Promote
    </button>
  )}
</td>

            </tr>
          ))}
        </tbody>
      </table>


      {/* FLAGGED POSTS */}
      {flaggedPosts.length > 0 && (
        <>
          <h3>Flagged Job Posts</h3>
          <table className="admin-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>User</th>
                <th>Result</th>
                <th>Text</th>
                <th>Time</th>
              </tr>
            </thead>
            <tbody>
              {flaggedPosts.map(p => (
                <tr key={p.id}>
                  <td>{p.id}</td>
                  <td>{p.user_id}</td>
                  <td>{p.result}</td>
                  <td>{p.text}</td>
                  <td>{p.created_at}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </>
      )}

    </div>
  
  );
}

export default AdminDashboard;
