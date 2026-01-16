import { useNavigate } from "react-router-dom";
import "../styles/home.css";

function Home() {
  const navigate = useNavigate();

  return (
    <div className="home-page">
      <div className="home-card">
        <h1>Fake Job Posting Detection</h1>
        <p>
          Detect fraudulent job postings using intelligent
          machine learning techniques and protect job seekers.
        </p>

        <div className="home-buttons">
          <button className="login-btn" onClick={() => navigate("/login")}>
            Login
          </button>

          <button className="signup-btn" onClick={() => navigate("/signup")}>
            Sign Up
          </button>
        </div>
      </div>
    </div>
  );
}

export default Home;
