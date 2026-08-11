import { Link } from "react-router-dom";

export default function Logo({ light = false }) {
  return (
    <Link to="/" className={`logo ${light ? "logo-light" : ""}`}>
      <span className="logo-mark">
        <span className="logo-bar logo-yellow"></span>
        <span className="logo-bar logo-teal"></span>
        <span className="logo-bar logo-blue"></span>
      </span>

      <span className="logo-text">Cognify</span>
    </Link>
  );
}