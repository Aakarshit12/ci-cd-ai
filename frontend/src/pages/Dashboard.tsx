import LetterGlitch from "../components/LetterGlitch";

export default function Dashboard() {
  return (
    <div className="relative min-h-screen overflow-hidden bg-zinc-900 text-white">
      {/* LetterGlitch background (NO vignette) */}
      <div className="absolute inset-0  pointer-events-none">
        <LetterGlitch
          glitchColors={["#2b4539","#61dca3","#61b3dc","#ffffff","#61dca3"]}
          centerVignette={false}
          outerVignette={false}
        />
      </div>

      {/* Foreground content */}
      <div className="relative z-10 min-h-screen p-6">
        <h1 className="text-2xl font-semibold mb-4">
          Dashboard
        </h1>

        <div className="rounded-xl border border-cyan-500/30 bg-black/40 p-6 backdrop-blur-md">
          Main application interface
        </div>
      </div>
    </div>
  );
}