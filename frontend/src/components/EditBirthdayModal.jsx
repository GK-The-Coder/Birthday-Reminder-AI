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
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);

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
      setError("");
      setSaving(true);
      try {
        await updateBirthday(birthday._id, formData);
        await refresh();
        onClose();
      } catch (error) {
        console.error(error);
        setError("Unable to update this birthday.");
      } finally {
        setSaving(false);
      }
    };

  return (
    <div className="modal-overlay">

      <div className="modal">

        <h2>
          Edit Birthday
        </h2>
        {error && <div className="form-error" role="alert">{error}</div>}

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
              disabled={saving}
            >
              {saving ? "Saving..." : "Save"}
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