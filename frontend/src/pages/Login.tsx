import { useState } from "react";
import FaultyTerminal from "../components/FaultyTerminalWrapper";
import { loginUser, signupUser } from "@/services/auth";

// Stable props for background so it doesn't re-render on every keystroke
const LOGIN_BG_GRID_MUL: [number, number] = [2, 1];

type LoginProps = {
  onLogin: () => void;
};

export default function Login({ onLogin }: LoginProps) {
  const [emailInput, setEmailInput] = useState("");
  const [passwordInput, setPasswordInput] = useState("");
  const [error, setError] = useState("");
  const [isSignup, setIsSignup] = useState(false);
  const [success, setSuccess] = useState("");

  return (
    <div className="relative min-h-screen overflow-hidden bg-zinc-900 text-white">
      {/* Background animation */}
      <div className="absolute inset-0">
        <FaultyTerminal
          scale={1.5}
          digitSize={1.2}
          gridMul={LOGIN_BG_GRID_MUL}
          timeScale={0.8}
          pageLoadAnimation={true}
          glitchAmount={0.6}
          flickerAmount={0.2}
          noiseAmp={1}
          scanlineIntensity={0.6}
          chromaticAberration={0}
          dither={0}
          curvature={0.1}
          mouseReact={true}
          mouseStrength={1.5}
          brightness={1.1}
          tint="#4ED454"
          className="opacity-55 pointer-events-auto"
        />
      </div>

      {/* Foreground */}
      <div className="relative z-10 flex min-h-screen items-center justify-center pointer-events-none">
        <div className="w-full max-w-md rounded-xl border border-white/15 bg-black/40 p-8 backdrop-blur-md pointer-events-auto">
          <h1 className="mb-6 text-center text-2xl font-semibold">
            {isSignup ? "Create account" : "Sign in"}
          </h1>

          <form
            className="space-y-4"
            onSubmit={async (e) => {
              e.preventDefault();
              setError("");
              setSuccess("");

              try {
                if (isSignup) {
                  await signupUser(emailInput, passwordInput);
                  setSuccess("Account created. You can sign in now.");
                  setIsSignup(false);
                } else {
                  const data = await loginUser(emailInput, passwordInput);
                  localStorage.setItem("token", data.access_token);
                  localStorage.setItem("user", JSON.stringify(data.user));
                  onLogin();
                }
              } catch (err: unknown) {
                const msg =
                  err && typeof err === "object" && "response" in err
                    ? (err as { response?: { data?: { detail?: string }; status?: number } }).response?.data?.detail
                    : null;
                const isNetwork =
                  err && typeof err === "object" && "response" in err
                    ? !(err as { response?: unknown }).response
                    : true;
                if (typeof msg === "string") setError(msg);
                else if (isNetwork)
                  setError("Cannot reach server. Is the backend running on http://localhost:8000?");
                else setError("Invalid credentials");
              }
            }}
          >
            <input
              type="email"
              placeholder="Email"
              value={emailInput}
              onChange={(e) => setEmailInput(e.target.value)}
              className="w-full rounded-md bg-zinc-900 px-4 py-2 text-white outline-none ring-1 ring-white/15 focus:ring-white/40"
            />

            <input
              type="password"
              placeholder="Password"
              value={passwordInput}
              onChange={(e) => setPasswordInput(e.target.value)}
              className="w-full rounded-md bg-zinc-900 px-4 py-2 text-white outline-none ring-1 ring-white/15 focus:ring-white/40"
            />

            {error && (
              <p className="text-sm text-red-400">{error}</p>
            )}
            {success && (
              <p className="text-sm text-green-400">{success}</p>
            )}

            <button
              type="submit"
              className="mt-2 w-full rounded-md bg-white py-2 font-medium text-black transition hover:bg-zinc-200"
            >
              {isSignup ? "Sign up" : "Login"}
            </button>

            <p className="text-center text-sm text-white/70">
              {isSignup ? "Already have an account? " : "No account? "}
              <button
                type="button"
                onClick={() => {
                  setIsSignup(!isSignup);
                  setError("");
                  setSuccess("");
                }}
                className="underline hover:text-white"
              >
                {isSignup ? "Sign in" : "Sign up"}
              </button>
            </p>
          </form>
        </div>
      </div>
    </div>
  );
}
