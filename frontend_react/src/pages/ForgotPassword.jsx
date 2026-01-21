import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { resetPassword } from "../services/authApi";
import "../styles/login.css";

function ForgotPassword() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const [error, setError] = useState("");

  const handleReset = async () => {
    if (!email || !password || !confirmPassword) {
      setError("All fields are required");
      return;
    }

    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    const res = await resetPassword({ email, password });

    if (res.message === "Password updated successfully") {
      alert("Password updated! Please login.");
      navigate("/login");
    } else {
      setError(res.message);
    }
  };

  return (
    <div className="login-page">
      <div className="login-card">
        <h2>Reset Password</h2>

        {error && <p className="error">{error}</p>}

        <input
          type="email"
          placeholder="Registered Email"
          onChange={(e) => setEmail(e.target.value)}
        />

       
        <div className="password-wrapper">
          <input
            type={showPassword ? "text" : "password"}
            placeholder="New Password"
            onChange={(e) => setPassword(e.target.value)}
          />
          <span
            className="eye-icon"
            onClick={() => setShowPassword(!showPassword)}
          >
            {showPassword ? "🙈" : "👁️"}
          </span>
        </div>

        <div className="password-wrapper">
          <input
            type={showConfirmPassword ? "text" : "password"}
            placeholder="Confirm New Password"
            onChange={(e) => setConfirmPassword(e.target.value)}
          />
          <span
            className="eye-icon"
            onClick={() =>
              setShowConfirmPassword(!showConfirmPassword)
            }
          >
            {showConfirmPassword ? "🙈" : "👁️"}
          </span>
        </div>

        <button onClick={handleReset}>Update Password</button>
      </div>
    </div>
  );
}

export default ForgotPassword;
