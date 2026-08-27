import { useState } from "react";
import { Navigate, Link } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

function Login() {
  const { login, token } = useAuth();
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState("");

  if (token) {
    return <Navigate to="/" replace />;
  }

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      await login(form);
    } catch (error) {
      console.error("Login error:", error);
      setError("Login failed. Check credentials.");
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card auth-card--dark">
        <div className="auth-header">
          <h2>Welcome back</h2>
          <p>Sign in to manage birthdays, wishes, and email reminders.</p>
        </div>

        <form onSubmit={handleSubmit}>
          <input name="email" type="email" placeholder="Email" value={form.email} onChange={handleChange} required />
          <input name="password" type="password" placeholder="Password" value={form.password} onChange={handleChange} required />
          {error && <div className="form-error">{error}</div>}
          <button type="submit">Continue</button>
        </form>

        <p className="auth-footer">
          New to WishMate? <Link to="/register">Create account</Link>
        </p>
      </div>
    </div>
  );
}

export default Login;
