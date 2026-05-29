/**
 * routes.jsx — App Routes
 *
 * Centralized route definitions.
 * Protected routes redirect to /login if not authenticated.
 */
import { Navigate, Route, Routes } from "react-router-dom";
import { useAuthStore } from "@/shared/store/authStore";
import LoginPage from "@/features/auth/pages/LoginPage";
import RegisterPage from "@/features/auth/pages/RegisterPage";
import DashboardPage from "@/features/dashboard/pages/DashboardPage";

function PrivateRoute({ children }) {
  const { isAuthenticated } = useAuthStore();
  return isAuthenticated ? children : <Navigate to="/login" replace />;
}

function PublicRoute({ children }) {
  const { isAuthenticated } = useAuthStore();
  return !isAuthenticated ? children : <Navigate to="/dashboard" replace />;
}

export default function AppRoutes() {
  return (
    <Routes>
      {/* Public */}
      <Route path="/login" element={<PublicRoute><LoginPage /></PublicRoute>} />
      <Route path="/register" element={<PublicRoute><RegisterPage /></PublicRoute>} />

      {/* Protected — dashboard será adicionado no próximo bloco */}
      <Route path="/dashboard" element={
        <PrivateRoute><DashboardPage /></PrivateRoute>
      } />

      {/* Fallback */}
      <Route path="*" element={<Navigate to="/login" replace />} />
    </Routes>
  );
}