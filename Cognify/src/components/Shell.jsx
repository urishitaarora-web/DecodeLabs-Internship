import { NavLink, Outlet, Link } from "react-router-dom";
import { useState } from "react";
import {
  BarChart3,
  BrainCircuit,
  Database,
  FileText,
  GitCompare,
  History,
  LayoutDashboard,
  Sparkles,
  Wrench,
} from "lucide-react";
import Logo from "./Logo";
import ThemeToggle from "./ThemeToggle";
import { useUser, useClerk } from "@clerk/react";

const nav = [
  ["Dashboard", "", LayoutDashboard],
  ["Datasets", "datasets", Database],
  ["Analysis", "analysis", BarChart3],
  ["Preprocessing", "preprocessing", Wrench],
  ["Training", "training", BrainCircuit],
  ["Evaluation", "evaluation", Sparkles],
  ["Comparison", "comparison", GitCompare],
  ["Prediction", "prediction", Sparkles],
  ["Explainable AI", "explainable", Sparkles],
  ["Reports", "reports", FileText],
  ["History", "history", History],
];

export default function Shell({ theme, toggleTheme }) {
  const { user } = useUser();
  const { signOut } = useClerk();

  const [profileOpen, setProfileOpen] = useState(false);

  const username =
    user?.username ||
    user?.firstName ||
    user?.primaryEmailAddress?.emailAddress?.split("@")[0] ||
    "User";

  const avatarLetter =
    user?.firstName?.[0] ||
    user?.username?.[0] ||
    user?.primaryEmailAddress?.emailAddress?.[0] ||
    "U";

  return (
    <div className="app-shell">

      {/* SIDEBAR */}
      <aside className="sidebar">
        <Logo light />

        <small className="workspace-label">
          ML WORKSPACE
        </small>

        <div className="side-label">
          WORKFLOW
        </div>

        <nav>
          {nav.map(([label, path, Icon]) => (
            <NavLink
              end={path === ""}
              key={label}
              to={"/app" + (path ? "/" + path : "")}
            >
              <Icon size={16} />
              <span>{label}</span>
            </NavLink>
          ))}
        </nav>

        <div className="side-bottom">
          <ThemeToggle
            theme={theme}
            onClick={toggleTheme}
          />

          <Link to="/">
            Back to website
          </Link>
        </div>
      </aside>

      {/* MAIN */}
      <main className="app-main">

        {/* TOP BAR */}
        <div className="app-top">

          <span>
            Workspace / <b>Overview</b>
          </span>

          <div className="profile-wrapper">

            {/* PROFILE BUTTON */}
            <button
              type="button"
              className="profile-button"
              onClick={() =>
                setProfileOpen((prev) => !prev)
              }
            >
              <div className="profile-avatar">
                {avatarLetter.toUpperCase()}
              </div>

              <div className="profile-name">
                <strong>
                  {username}
                </strong>

                <small>
                  Profile
                </small>
              </div>

              <span className="profile-arrow">
                {profileOpen ? "▲" : "▼"}
              </span>
            </button>

            {/* DROPDOWN */}
            {profileOpen && (
              <div className="profile-dropdown">

                <div className="profile-dropdown-header">

                  <strong>
                    {username}
                  </strong>

                  <small>
                    {user?.primaryEmailAddress?.emailAddress}
                  </small>

                </div>

                <button
                  type="button"
                  className="profile-dropdown-item"
                  onClick={async () => {
                    setProfileOpen(false);

                    await signOut({
                      redirectUrl: "/auth",
                    });
                  }}
                >
                  Sign out
                </button>

              </div>
            )}

          </div>

        </div>

        <Outlet />

      </main>
    </div>
  );
}