import FaultyTerminal from "../components/FaultyTerminal";

export default function Login() {
  return (
    <div className="relative min-h-screen overflow-hidden bg-background">
      {/* Background terminal */}
      <div className="absolute inset-0 opacity-60 pointer-events-none">
        <FaultyTerminal />
      </div>

      {/* Foreground login card */}
      <div className="relative z-10 flex min-h-screen items-center justify-center">
        <div className="w-full max-w-md rounded-xl border border-white/15 bg-black/40 p-8 backdrop-blur-md">
          <h2 className="mb-6 text-center text-2xl font-semibold text-white">
            Sign in
          </h2>

          <form className="space-y-4">
            <input
              type="email"
              placeholder="Email"
              className="w-full rounded-md bg-zinc-900 px-4 py-2 text-white outline-none ring-1 ring-white/15 focus:ring-white/40"
            />

            <input
              type="password"
              placeholder="Password"
              className="w-full rounded-md bg-zinc-900 px-4 py-2 text-white outline-none ring-1 ring-white/15 focus:ring-white/40"
            />

            <button
              type="submit"
              className="w-full rounded-md bg-white py-2 font-medium text-black hover:bg-zinc-200"
            >
              Login
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
