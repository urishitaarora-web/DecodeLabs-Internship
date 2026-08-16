import { Link } from "react-router-dom";
import { ArrowUpRight } from "lucide-react";
import Logo from "./Logo";
import ThemeToggle from "./ThemeToggle";

export default function Navbar({ theme, toggleTheme }) {
  return (
    <header className="navbar">
      <Logo />
      <nav>
        <a href="#product">Product</a>
        <a href="#features">Features</a>
        <a href="#workflow">Workflow</a>
        <a href="#solutions">Solutions</a>
        <a href="#resources">Resources</a>
      </nav>
      <div className="nav-actions">
        <ThemeToggle theme={theme} onClick={toggleTheme} />
        <Link className="login-link" to="/auth">Log in</Link>
        <Link className="btn btn-primary btn-sm" to="/auth">Get Started <ArrowUpRight size={15}/></Link>
      </div>
    </header>
  );
}