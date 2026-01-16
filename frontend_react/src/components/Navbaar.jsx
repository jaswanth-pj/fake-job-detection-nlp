import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/navbaar.css";

function Navbaar() {
  const navigate = useNavigate();
  const [open, setOpen] = useState(false);

  const email = localStorage.getItem("userEmail");
  const role = localStorage.getItem("role");

  const handleLogout = () => {
    localStorage.clear();
    navigate("/login");
  };

  return (
    <nav className="navbar">
      {/* LEFT */}
      <div className="nav-left">
        Fake Job Detection
      </div>

      {/* RIGHT */}
      <div className="nav-right">
        {/* 🔥 WRAPPER IS THE KEY FIX */}
        <div className="user-wrapper">
          <div
            className="user-profile"
            onClick={() => setOpen(!open)}
          >
            {email || "User"}
          </div>

          {open && (
            <div className="dropdown">

              {/* 🔐 ADMIN ONLY */}
              {role === "admin" && (
                <div
                  className="dropdown-item admin-item"
                  onClick={() => {
                    navigate("/admin");
                    setOpen(false);
                  }}
                >
                  🛡️ Admin Dashboard
                </div>
              )}

              <div
                className="dropdown-item"
                onClick={() => {
                  navigate("/dashboard");
                  setOpen(false);
                }}
              >
                👤 User Dashboard
              </div>

              <div
                className="dropdown-item"
                onClick={() => {
                  navigate("/history");
                  setOpen(false);
                }}
              >
                📜 Prediction History
              </div>

              <hr />

              <div
                className="dropdown-item logout"
                onClick={handleLogout}
              >
                🚪 Logout
              </div>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
}

export default Navbaar;
