import { useMemo, useState } from "react";
import { deleteBirthday, generateWish } from "../services/birthdayApi";
import WishModal from "./WishModal";

function BirthdayCard({ birthday, refresh, onEdit }) {
  const [wish, setWish] = useState(null);
  const [error, setError] = useState("");
  const [deleting, setDeleting] = useState(false);
  const [generating, setGenerating] = useState(false);

  const dateLabel = useMemo(() => {
    const date = new Date(birthday.birthday);
    return date.toLocaleDateString(undefined, { month: "short", day: "numeric", year: "numeric" });
  }, [birthday.birthday]);

  const handleDelete = async () => {
    setError("");
    setDeleting(true);
    try {
      await deleteBirthday(birthday._id);
      await refresh();
    } catch (error) {
      console.error(error);
      setError("Unable to delete this birthday.");
    } finally {
      setDeleting(false);
    }
  };

  const handleWish = async () => {
    setError("");
    setGenerating(true);
    try {
      const response = await generateWish(birthday.name);
      setWish(response.data.wish);
    } catch (error) {
      console.error(error);
      setError("Unable to generate a wish right now.");
    } finally {
      setGenerating(false);
    }
  };

  return (
    <>
      <div className="card">
        <div className="badge">Upcoming</div>
        <h3>{birthday.name}</h3>
        <p>{birthday.email}</p>
        <p>{dateLabel}</p>
        {error && <div className="form-error" role="alert">{error}</div>}

        <div className="card-buttons">
          <button className="edit-btn" onClick={() => onEdit(birthday)}>
            Edit
          </button>
          <button className="delete-btn" onClick={handleDelete} disabled={deleting}>
            {deleting ? "Deleting..." : "Delete"}
          </button>
          <button className="wish-btn" onClick={handleWish} disabled={generating}>
            {generating ? "Generating..." : "✨ Generate wish"}
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