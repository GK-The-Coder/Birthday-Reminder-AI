import { useState } from "react";
import { updateBirthday } from "../services/birthdayApi";

function EditBirthdayModal({
  birthday,
  onClose,
  refresh,
}) {
  const [formData, setFormData] =
    useState({
      name: birthday.name,
      email: birthday.email,
      birthday:
        birthday.birthday,
    });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]:
        e.target.value,
    });
  };

  const handleSubmit =
    async (e) => {
      e.preventDefault();

      await updateBirthday(
        birthday._id,
        formData
      );

      refresh();

      onClose();
    };

  return (
    <div className="modal-overlay">

      <div className="modal">

        <h2>
          Edit Birthday
        </h2>

        <form
          onSubmit={
            handleSubmit
          }
        >

          <input
            type="text"
            name="name"
            value={
              formData.name
            }
            onChange={
              handleChange
            }
          />

          <input
            type="email"
            name="email"
            value={
              formData.email
            }
            onChange={
              handleChange
            }
          />

          <input
            type="date"
            name="birthday"
            value={
              formData.birthday
            }
            onChange={
              handleChange
            }
          />

          <div className="modal-buttons">

            <button
              type="submit"
            >
              Save
            </button>

            <button
              type="button"
              onClick={
                onClose
              }
            >
              Cancel
            </button>

          </div>

        </form>

      </div>

    </div>
  );
}

export default EditBirthdayModal;