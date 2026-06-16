import { useEffect, useMemo, useState } from "react";

import Navbar from "../components/Navbar";
import BirthdayCard from "../components/BirthdayCard";
import BirthdayForm from "../components/BirthdayForm";
import StatsCard from "../components/StatsCard";
import SearchBar from "../components/SearchBar";
import EditBirthdayModal from "../components/EditBirthdayModal";
import EmailLogs from "../components/EmailLogs";
import Footer from "../components/Footer";

import { getBirthdays, getStats, getLogs } from "../services/birthdayApi";

function Dashboard() {
  const [birthdays, setBirthdays] = useState([]);
  const [search, setSearch] = useState("");
  const [selectedBirthday, setSelectedBirthday] = useState(null);
  const [stats, setStats] = useState({});
  const [logs, setLogs] = useState([]);

  const loadBirthdays = async () => {
    try {
      const response = await getBirthdays();
      setBirthdays(response.data);
    } catch (error) {
      console.error("Failed to load birthdays", error);
    }
  };

  const loadStats = async () => {
    try {
      const response = await getStats();
      setStats(response.data);
    } catch (error) {
      console.error("Failed to load stats", error);
    }
  };

  const loadLogs = async () => {
    try {
      const response = await getLogs();
      setLogs(response.data);
    } catch (error) {
      console.error("Failed to load logs", error);
    }
  };

  useEffect(() => {
    loadBirthdays();
    loadStats();
    loadLogs();
  }, []);

  const upcomingBirthday = useMemo(() => {
    if (!birthdays.length) return null;
    const sorted = [...birthdays].sort((a, b) => new Date(a.birthday) - new Date(b.birthday));
    return sorted[0];
  }, [birthdays]);

  const filteredBirthdays = birthdays.filter((birthday) =>
    birthday.name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="dashboard-shell">
      <Navbar />

      <main className="container">
        <section className="hero-panel">
          <div>
            <span className="eyebrow">Birthday Reminder AI</span>
            <h2>Your birthday command center</h2>
            <p>
              Manage celebrations, generate thoughtful wishes, and automate reminder emails from one premium dashboard.
            </p>
          </div>

          <div className="hero-card">
            <div>
              <p className="hero-label">Next celebration</p>
              <h3>{upcomingBirthday ? upcomingBirthday.name : "No upcoming birthdays"}</h3>
              <p>{upcomingBirthday ? upcomingBirthday.birthday : "Add a birthday to get started."}</p>
            </div>
            <div className="hero-stats">
              <div>
                <span>{stats.todayBirthdays || 0}</span>
                <p>Today</p>
              </div>
              <div>
                <span>{stats.thisMonth || 0}</span>
                <p>This month</p>
              </div>
            </div>
          </div>
        </section>

        <section className="stats-grid">
          <StatsCard title="Total birthdays" value={stats.totalBirthdays || 0} />
          <StatsCard title="Upcoming this month" value={stats.thisMonth || 0} />
          <StatsCard title="Emails sent" value={stats.emailsSent || 0} />
          <StatsCard title="Today" value={stats.todayBirthdays || 0} />
        </section>

        <section className="dashboard-grid">
          <div className="dashboard-column dashboard-column--large">
            <div className="panel panel--glow">
              <div className="panel-header">
                <h3>Birthday list</h3>
                <span>{filteredBirthdays.length} reminders</span>
              </div>
              <SearchBar search={search} setSearch={setSearch} />
              <div className="birthday-grid">
                {filteredBirthdays.length > 0 ? (
                  filteredBirthdays.map((birthday) => (
                    <BirthdayCard
                      key={birthday._id}
                      birthday={birthday}
                      refresh={loadBirthdays}
                      onEdit={setSelectedBirthday}
                    />
                  ))
                ) : (
                  <div className="empty-state">No birthdays found. Add your first reminder.</div>
                )}
              </div>
            </div>

            <div className="panel panel--glass">
              <EmailLogs logs={logs} />
            </div>
          </div>

          <div className="dashboard-column dashboard-column--sidebar">
            <div className="panel panel--glass">
              <BirthdayForm refresh={loadBirthdays} />
            </div>
          </div>
        </section>

        {selectedBirthday && (
          <EditBirthdayModal
            birthday={selectedBirthday}
            refresh={loadBirthdays}
            onClose={() => setSelectedBirthday(null)}
          />
        )}
      </main>

      <Footer />
    </div>
  );
}

export default Dashboard;
