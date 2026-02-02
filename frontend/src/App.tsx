import FaultyTerminal from "./components/FaultyTerminal";

function App() {
  return (
    <div className="relative min-h-screen overflow-hidden bg-zinc-900 text-white">
      {/* FaultyTerminal background */}
      <div className="absolute inset-0">
        <FaultyTerminal
          scale={1.5}
          digitSize={1.2}
          gridMul={[2, 1]}
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

      {/* Foreground content */}
      <div className="relative z-10 flex min-h-screen items-center justify-center pointer-events-none">
        <div className="w-full max-w-md rounded-xl border border-white/15 bg-black/40 p-8 backdrop-blur-md pointer-events-auto">
          <h1 className="mb-6 text-center text-2xl font-semibold">
            Sign in
          </h1>

          <form className="space-y-4">
            {/* User ID */}
            <input
              type="text"
              placeholder="User ID"
              className="w-full rounded-md bg-zinc-900 px-4 py-2 text-white outline-none ring-1 ring-white/15 focus:ring-white/40"
            />

            {/* Password */}
            <input
              type="password"
              placeholder="Password"
              className="w-full rounded-md bg-zinc-900 px-4 py-2 text-white outline-none ring-1 ring-white/15 focus:ring-white/40"
            />

            {/* Submit */}
            <button
              type="submit"
              className="mt-2 w-full rounded-md bg-white py-2 font-medium text-black transition hover:bg-zinc-200"
            >
              Login
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default App;
