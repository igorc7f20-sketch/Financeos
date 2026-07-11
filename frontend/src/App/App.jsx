/**
 * App.jsx — Application Root
 * Provides router and theme context.
 */
import { useEffect } from "react";
import { BrowserRouter } from "react-router-dom";
import { useTheme } from "@/shared/hooks/useTheme";
import { useAuthStore } from "@/shared/store/authStore";
import AppRoutes from "./routes";

export default function App() {
  useTheme(); // aplica dark/light no <html>
  const initializeAuth = useAuthStore((state) => state.initializeAuth);

  useEffect(() => {
    initializeAuth();
  }, [initializeAuth]);

  return (
    <BrowserRouter>
      <AppRoutes />
    </BrowserRouter>
  );
}