import { useState } from "react";
import FaultyTerminal from "../components/FaultyTerminalWrapper";
import { loginUser, signupUser } from "../services/auth";

const LOGIN_BG_GRID_MUL: [number, number] = [2, 1];

type LoginProps = {
  onLogin: () => void;
};

const validatePassword = (password: string): string | null => {
  if (password.length < 8) return "Password must be at least 8 characters long";
  if (!/[A-Za-z]/.test(password))
    return "Password must contain at least one letter";
  if (!/[0-9]/.test(password))
    return "Password must contain at least one number";
  return null;
};

export default function Login({ onLogin }: LoginProps) {
  const [emailInput, setEmailInput] = useState("");
  const [passwordInput, setPasswordInput] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [passwordError, setPasswordError] = useState("");
  const [isSignup, setIsSignup] = useState(false);
  const [loading, setLoading] = useState(false);

  return (
    <div className="relative min-h-screen overflow-hidden bg-zinc-900 text-white">
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

      <div className="relative z-10 flex min-h-screen items-center justify-center pointer-events-none">
        <div className="w-full max-w-md rounded-xl border border-white/15 bg-black/40 p-8 backdrop-blur-md pointer-events-auto">
          <h1 className="mb-6 text-center text-2xl font-semibold">
            {isSignup ? "Create account" : "Sign in"}
          </h1>

          <form
            className="space-y-4"
            onSubmit={async (e) => {
              e.preventDefault();
              if (loading) return;

              setError("");
              setSuccess("");
              setPasswordError("");
              setLoading(true);

              try {
                if (isSignup) {
                  const err = validatePassword(passwordInput);
                  if (err) {
                    setPasswordError(err);
                    setLoading(false);
                    return;
                  }

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
                    ? (err as { response?: { data?: { detail?: string } } })
                        .response?.data?.detail
                    : null;

                const isNetwork =
                  err && typeof err === "object" && "response" in err
                    ? !(err as { response?: unknown }).response
                    : true;

                if (typeof msg === "string") setError(msg);
                else if (isNetwork)
                  setError(
                    "Cannot reach server. Is the backend running on http://localhost:8000?"
                  );
                else setError("Invalid credentials");
              } finally {
                setLoading(false);
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

            <div className="relative">
              <input
                type={showPassword ? "text" : "password"}
                placeholder="Password"
                value={passwordInput}
                onChange={(e) => {
                  const val = e.target.value;
                  setPasswordInput(val);
                  if (isSignup) {
                    const err = validatePassword(val);
                    setPasswordError(err ?? "");
                  }
                }}
                className="w-full rounded-md bg-zinc-900 px-4 py-2 pr-12 text-white outline-none ring-1 ring-white/15 focus:ring-white/40"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-2 text-sm text-white/60 hover:text-white"
              >
                {showPassword ? "Hide" : "Show"}
              </button>
            </div>

            {passwordError && (
              <p className="text-sm text-yellow-400">{passwordError}</p>
            )}
            {error && <p className="text-sm text-red-400">{error}</p>}
            {success && <p className="text-sm text-green-400">{success}</p>}

            <button
              type="submit"
              disabled={loading}
              className="mt-2 w-full rounded-md bg-white py-2 font-medium text-black transition hover:bg-zinc-200 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading
                ? isSignup
                  ? "Creating account..."
                  : "Signing in..."
                : isSignup
                ? "Sign up"
                : "Login"}
            </button>

            <p className="text-center text-sm text-white/70">
              {isSignup ? "Already have an account? " : "No account? "}
              <button
                type="button"
                onClick={() => {
                  if (loading) return;
                  setIsSignup(!isSignup);
                  setError("");
                  setSuccess("");
                  setPasswordError("");
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
