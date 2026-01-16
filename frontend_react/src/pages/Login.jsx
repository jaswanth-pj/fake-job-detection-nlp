import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { loginUser } from "../services/authApi";
import "../styles/login.css";

function Login() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");

  const handleLogin = async () => {
    if (!email || !password) {
      setError("Please enter email and password");
      return;
    }

    try {
      const res = await loginUser({ email, password });

      if (res.message === "Login successful") {
        localStorage.setItem("isLoggedIn", "true");
        localStorage.setItem("userEmail", email);
        localStorage.setItem("userId", res.user_id);
        localStorage.setItem("role", res.role);
        navigate("/detect");
      } else {
        setError(res.message);
      }
    } catch (err) {
      setError("Server error. Try again later.");
    }
  };

  return (
    <div className="login-page">
      <div className="login-card">
        <h2>Login</h2>

        {error && <p className="error">{error}</p>}

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        {/* Password with Eye Icon */}
        <div className="password-wrapper">
          <input
            type={showPassword ? "text" : "password"}
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <span
            className="eye-icon"
            onClick={() => setShowPassword(!showPassword)}
          >
            {showPassword ? "🙈" : "👁️"}
          </span>
        </div>

        <button onClick={handleLogin}>Login</button>

        <p
          className="forgot-text"
          onClick={() => navigate("/forgot-password")}
        >
          Forgot password?
        </p>

        <p className="signup-text">
          Don’t have an account?{" "}
          <span onClick={() => navigate("/signup")}>Sign up</span>
        </p>
      </div>
    </div>
  );
}

export default Login;
