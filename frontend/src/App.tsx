import { useEffect, useState } from "react";
import Login from "./pages/Login";
import ProtectedLayout from "./layouts/ProtectedLayout";
import Dashboard from "./pages/Dashboard";
import { getMe } from "@/services/auth";

function App() {
  const token = localStorage.getItem("token");

  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(Boolean(token));

  useEffect(() => {
    if (!token) return;

    getMe()
      .then(() => {
        setIsAuthenticated(true);
      })
      .catch(() => {
        localStorage.removeItem("token");
        localStorage.removeItem("user");
        setIsAuthenticated(false);
      })
      .finally(() => {
        setLoading(false);
      });
  }, [token]);

  if (loading) return null;

  if (!token || !isAuthenticated) {
    return <Login onLogin={() => setIsAuthenticated(true)} />;
  }

  return (
    <ProtectedLayout>
      <Dashboard />
    </ProtectedLayout>
  );
}

export default App;
