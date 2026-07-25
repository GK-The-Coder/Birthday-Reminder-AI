import { useState } from "react";
import { Navigate, Link } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

function Register() {
  const { register, token } = useAuth();
  const [form, setForm] = useState({ name: "", email: "", password: "" });
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  if (token) {
    return <Navigate to="/" replace />;
  }

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      await register(form);
      setSuccess(true);
    } catch (error) {
      console.error("Registration error:", error);
      setError("Registration failed. Try again.");
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card auth-card--dark">
        <div className="auth-header">
          <h2>Create your account</h2>
          <p>Get started with Birthday Reminder AI in seconds.</p>
        </div>

        {success ? (
          <div className="auth-success">
            Registration successful! <Link to="/login">Sign in now</Link>
          </div>
        ) : (
          <form onSubmit={handleSubmit}>
            <input name="name" placeholder="Full name" value={form.name} onChange={handleChange} required />
            <input name="email" type="email" placeholder="Email" value={form.email} onChange={handleChange} required />
            <input name="password" type="password" placeholder="Password" value={form.password} onChange={handleChange} required />
            {error && <div className="form-error">{error}</div>}
            <button type="submit">Create account</button>
          </form>
        )}

        <p className="auth-footer">
          Already have an account? <Link to="/login">Log in</Link>
        </p>
      </div>
    </div>
  );
}

export default Register;
