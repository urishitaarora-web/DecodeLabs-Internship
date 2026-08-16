import React, { useEffect, useState } from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import { useAuth } from "@clerk/react";

import Landing from "./pages/Landing";
import Dashboard from "./pages/Dashboard";
import WorkspacePage from "./pages/WorkspacePage";
import Shell from "./components/Shell";
import Auth from "./pages/Auth";


function ProtectedRoute({ children }) {
  const { isLoaded, isSignedIn } = useAuth();

  if (!isLoaded) {
    return <div>Loading...</div>;
  }

  if (!isSignedIn) {
    return <Navigate to="/auth" replace />;
  }

  return children;
}


export default function App() {

  const [theme, setTheme] = useState(
    () =>
      localStorage.getItem("cognify-theme") || "light"
  );


  useEffect(() => {
    document.documentElement.dataset.theme = theme;

    localStorage.setItem(
      "cognify-theme",
      theme
    );
  }, [theme]);


  const toggleTheme = () => {
    setTheme((v) =>
      v === "light" ? "dark" : "light"
    );
  };


  return (
    <Routes>

      {/* LANDING PAGE */}
      <Route
        path="/"
        element={
          <Landing
            theme={theme}
            toggleTheme={toggleTheme}
          />
        }
      />


      {/* AUTH PAGE */}
      <Route
        path="/auth"
        element={<Auth />}
      />


      {/* PROTECTED APPLICATION */}
      <Route
        path="/app"
        element={
          <ProtectedRoute>
            <Shell
              theme={theme}
              toggleTheme={toggleTheme}
            />
          </ProtectedRoute>
        }
      >

        <Route
          index
          element={<Dashboard />}
        />

        <Route
          path=":page"
          element={<WorkspacePage />}
        />

      </Route>


      {/* FALLBACK */}
      <Route
        path="*"
        element={
          <Navigate
            to="/"
            replace
          />
        }
      />

    </Routes>
  );
}