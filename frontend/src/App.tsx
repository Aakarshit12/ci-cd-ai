import { useState } from "react";
import Login from "./pages/Login";
import ProtectedLayout from "./layouts/ProtectedLayout";
import Dashboard from "./pages/Dashboard";

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

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
