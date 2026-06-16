// src/pages/AddBirthday.jsx

import { useState } from "react";
import { addBirthday } from "../services/birthdayApi";

function AddBirthday() {

  const [formData, setFormData] = useState({
    name: "",
    email: "",
    birthday: ""
  });

  const handleChange = (e) => {

    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });

  };

  const handleSubmit = async (e) => {

    e.preventDefault();

    try {

      await addBirthday(formData);

      alert("Birthday Added");

      setFormData({
        name: "",
        email: "",
        birthday: ""
      });

    } catch (error) {

      console.log(error);

    }

  };

  return (
    <div>

      <h2>Add Birthday</h2>

      <form onSubmit={handleSubmit}>

        <input
          type="text"
          name="name"
          placeholder="Name"
          value={formData.name}
          onChange={handleChange}
        />

        <br /><br />

        <input
          type="email"
          name="email"
          placeholder="Email"
          value={formData.email}
          onChange={handleChange}
        />

        <br /><br />

        <input
          type="date"
          name="birthday"
          value={formData.birthday}
          onChange={handleChange}
        />

        <br /><br />

        <button type="submit">
          Add Birthday
        </button>

      </form>

    </div>
  );
}

export default AddBirthday;