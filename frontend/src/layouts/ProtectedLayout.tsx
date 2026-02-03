// layouts/ProtectedLayout.tsx
export default function ProtectedLayout({ children }: { children: React.ReactNode }) {
    return (
      <div className="min-h-screen bg-zinc-900 text-white">
        {/* Later: Navbar / Sidebar */}
        {children}
      </div>
    );
  }
  