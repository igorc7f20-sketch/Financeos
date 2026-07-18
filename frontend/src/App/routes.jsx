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
import CashPage from "@/features/cash/pages/CashPage";
import AppLayout from "@/shared/components/AppLayout";
import PayablesPage from "../features/payables/pages/PayablesPage";

function PrivateRoute({ children }) {
  const { isAuthenticated } = useAuthStore();
  if (!isAuthenticated) return <Navigate to="/login" replace />;
  return <AppLayout>{children}</AppLayout>;
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
      
      <Route path="/cash" element={
        <PrivateRoute><CashPage /></PrivateRoute>
      } />

      {/* Fallback */}
      <Route path="*" element={<Navigate to="/login" replace />} />

      <Route path="/payables" element={<PrivateRoute><PayablesPage /></PrivateRoute>} />
    </Routes>
  );
}