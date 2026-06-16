import { useMemo, useState } from "react";
import { deleteBirthday, generateWish } from "../services/birthdayApi";
import WishModal from "./WishModal";

function BirthdayCard({ birthday, refresh, onEdit }) {
  const [wish, setWish] = useState(null);

  const dateLabel = useMemo(() => {
    const date = new Date(birthday.birthday);
    return date.toLocaleDateString(undefined, { month: "short", day: "numeric", year: "numeric" });
  }, [birthday.birthday]);

  const handleDelete = async () => {
    await deleteBirthday(
      birthday._id
    );

    refresh();
  };

  const handleWish = async () => {
    try {
      const response = await generateWish(birthday.name);
      setWish(response.data.wish);
    } catch (error) {
      console.error(error);
      alert("Unable to generate a wish right now.");
    }
  };

  return (
    <>
      <div className="card">
        <div className="badge">Upcoming</div>
        <h3>{birthday.name}</h3>
        <p>{birthday.email}</p>
        <p>{dateLabel}</p>

        <div className="card-buttons">
          <button className="edit-btn" onClick={() => onEdit(birthday)}>
            Edit
          </button>
          <button className="delete-btn" onClick={handleDelete}>
            Delete
          </button>
          <button className="wish-btn" onClick={handleWish}>
            ✨ Generate wish
          </button>
        </div>
      </div>

      {wish && (
        <WishModal wish={wish} birthday={birthday} onClose={() => setWish(null)} />
      )}
    </>
  );
}

export default BirthdayCard;