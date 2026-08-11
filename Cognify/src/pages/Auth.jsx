import { SignIn, SignUp } from "@clerk/react";
import { useState } from "react";

export default function Auth() {
  const [mode, setMode] = useState("login");

  return (
    <div className="auth-page">
      {mode === "login" ? (
        <SignIn
          routing="path"
          path="/auth"
          signUpUrl="/auth"
          forceRedirectUrl="/app"
        />
      ) : (
        <SignUp
          routing="path"
          path="/auth"
          signInUrl="/auth"
          forceRedirectUrl="/app"
        />
      )}
    </div>
  );
}