import { useState } from "react";
import { sendBirthdayEmail }
from "../services/birthdayApi";

function WishModal({
  wish,
  birthday,
  onClose,
}) {
  const [error, setError] = useState("");
  const [sending, setSending] = useState(false);

  const copyWish = () => {

    navigator.clipboard.writeText(
      wish
    );

    alert(
      "Copied!"
    );

  };

  const handleSend =
    async () => {
      setError("");
      setSending(true);
      try {

        await sendBirthdayEmail({

          name:
            birthday.name,

          email:
            birthday.email

        });

        alert("Email Sent Successfully!");

      } catch (error) {
        console.log(error);
        setError("Failed to send email. Please try again.");
      } finally {
        setSending(false);

      }

    };

  return (

    <div className="modal-overlay">

      <div className="modal">

        <h2>
          ✨ AI Generated Wish
        </h2>

        <div className="wish-content">
          {wish}
        </div>
        {error && <div className="form-error" role="alert">{error}</div>}

        <div className="modal-buttons">

          <button
            onClick={copyWish}
          >
            Copy
          </button>

          <button
            onClick={handleSend}
            disabled={sending}
          >
            {sending ? "Sending..." : "Send Email"}
          </button>

          <button
            onClick={onClose}
          >
            Close
          </button>

        </div>

      </div>

    </div>

  );
}

export default WishModal;