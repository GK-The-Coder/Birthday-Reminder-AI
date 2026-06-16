import { sendBirthdayEmail }
from "../services/birthdayApi";

function WishModal({
  wish,
  birthday,
  onClose,
}) {

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

      try {

        await sendBirthdayEmail({

          name:
            birthday.name,

          email:
            birthday.email

        });

        alert(
          "Email Sent Successfully!"
        );

      } catch (error) {

        console.log(error);

        alert(
          "Failed to send email"
        );

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

        <div className="modal-buttons">

          <button
            onClick={copyWish}
          >
            Copy
          </button>

          <button
            onClick={handleSend}
          >
            Send Email
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