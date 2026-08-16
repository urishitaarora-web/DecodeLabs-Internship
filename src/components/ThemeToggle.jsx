import { Moon, Sun } from "lucide-react";

export default function ThemeToggle({ theme, onClick }) {
  return (
    <button className="icon-btn" onClick={onClick} aria-label={`Switch to ${theme === "light" ? "dark" : "light"} theme`}>
      {theme === "light" ? <Moon size={16} /> : <Sun size={16} />}
    </button>
  );
}