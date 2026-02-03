// layouts/PublicLayout.tsx
export default function PublicLayout({ children }: { children: React.ReactNode }) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-zinc-900 text-white">
        {children}
      </div>
    );
  }
  