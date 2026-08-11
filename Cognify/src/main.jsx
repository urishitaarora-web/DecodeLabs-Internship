import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { ClerkProvider } from "@clerk/react";

import App from "./App";
import "./styles.css";


ReactDOM.createRoot(
  document.getElementById("root")
).render(

  <React.StrictMode>

    <ClerkProvider
      publishableKey={
        import.meta.env.VITE_CLERK_PUBLISHABLE_KEY
      }
    >

      <BrowserRouter>
        <App />
      </BrowserRouter>

    </ClerkProvider>

  </React.StrictMode>
);