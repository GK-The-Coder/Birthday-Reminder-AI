import { useState } from "react";
import { addBirthday } from "../services/birthdayApi";

function BirthdayForm({ refresh }) {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    birthday: "",
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    await addBirthday(formData);
    setFormData({ name: "", email: "", birthday: "" });
    refresh();
  };

  return (
    <form className="form" onSubmit={handleSubmit}>
      <h2>Add new birthday</h2>
      <p className="form-subtitle">Add a person and send automated celebration reminders.</p>
      <input type="text" name="name" placeholder="Name" value={formData.name} onChange={handleChange} required />
      <input type="email" name="email" placeholder="Email" value={formData.email} onChange={handleChange} required />
      <input type="date" name="birthday" value={formData.birthday} onChange={handleChange} required />
      <button type="submit">Save reminder</button>
    </form>
  );
}

export default BirthdayForm;