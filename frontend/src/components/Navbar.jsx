import { useAuth } from "../context/AuthContext";

function Navbar() {
  const { logout } = useAuth();

  return (
    <header className="navbar">

      <div className="navbar-brand">
        <div className="brand-mark">🎂</div>
        <div>
          <h1>Birthday Reminder AI</h1>
          <p>Premium birthday tracking and celebration automation.</p>
        </div>
      </div>
      <button className="logout-btn" onClick={logout}>
        Sign out
      </button>
    </header>
  );
}

export default Navbar;