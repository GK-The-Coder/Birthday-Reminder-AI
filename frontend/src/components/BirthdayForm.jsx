import { useState } from "react";
import { addBirthday } from "../services/birthdayApi";

function BirthdayForm({ refresh }) {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    birthday: "",
  });
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSaving(true);
    try {
      await addBirthday(formData);
      setFormData({ name: "", email: "", birthday: "" });
      await refresh();
    } catch (error) {
      setError(error.response?.data?.detail || "Unable to save birthday.");
    } finally {
      setSaving(false);
    }
  };

  return (
    <form className="form" onSubmit={handleSubmit}>
      <h2>Add new birthday</h2>
      <p className="form-subtitle">Add a person and send automated celebration reminders.</p>
      <input type="text" name="name" placeholder="Name" value={formData.name} onChange={handleChange} required />
      <input type="email" name="email" placeholder="Email" value={formData.email} onChange={handleChange} required />
      <input type="date" name="birthday" value={formData.birthday} onChange={handleChange} required />
      {error && <div className="form-error" role="alert">{error}</div>}
      <button type="submit" disabled={saving}>{saving ? "Saving..." : "Save reminder"}</button>
    </form>
  );
}

export default BirthdayForm;