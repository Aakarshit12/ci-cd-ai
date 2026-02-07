import { useState } from "react";
import { registerUser, loginUser } from "../services/auth";

type SignupProps = {
  onLogin: () => void;
};

export default function Signup({ onLogin }: SignupProps) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      // 1️⃣ create account
      await registerUser(email, password);

      // 2️⃣ auto login
      const data = await loginUser(email, password);

      // 3️⃣ store auth
      localStorage.setItem("token", data.access_token);
      localStorage.setItem("user", JSON.stringify(data.user));

      // 4️⃣ enter app
      onLogin();
    } catch (err: any) {
      setError(err?.response?.data?.detail || "Signup failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSignup}>
      <input value={email} onChange={e => setEmail(e.target.value)} />
      <input
        type="password"
        value={password}
        onChange={e => setPassword(e.target.value)}
      />

      {error && <p>{error}</p>}

      <button disabled={loading}>
        {loading ? "Creating account..." : "Sign up"}
      </button>
    </form>
  );
}
