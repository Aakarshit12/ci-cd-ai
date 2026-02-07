// layouts/ProtectedLayout.tsx
export default function ProtectedLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    window.location.reload();
  };

  return (
    <div className="relative min-h-screen bg-zinc-900 text-white">
      {/* Logout overlay (background only, not layout) */}
      <button
        onClick={handleLogout}
        className="fixed top-4 right-4 z-50 rounded bg-red-500/80 backdrop-blur px-4 py-1 text-sm hover:bg-red-600"

      >
        Logout
      </button>

      {/* Protected content */}
      {children}
    </div>
  );
}
