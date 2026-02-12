import { useEffect, useState } from "react";
import Login from "./pages/Login";
import ProtectedLayout from "./layouts/ProtectedLayout";
import Dashboard from "./pages/Dashboard";
import { getMe } from "@/services/auth";

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("token");

    if (!token) {
      setLoading(false);
      return;
    }

    // validate token with backend
    getMe()
      .then(() => setIsAuthenticated(true))
      .catch(() => {
        localStorage.removeItem("token");
        localStorage.removeItem("user");
        setIsAuthenticated(false);
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) return null;

  if (!isAuthenticated) {
    return <Login onLogin={() => setIsAuthenticated(true)} />;
  }

  return (
    <ProtectedLayout>
      <Dashboard />
    </ProtectedLayout>
  );
}

export default App;
