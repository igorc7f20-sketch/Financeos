/**
 * App.jsx — Application Root
 * Provides router and theme context.
 */
import { BrowserRouter } from "react-router-dom";
import { useTheme } from "@/shared/hooks/useTheme";
import AppRoutes from "./routes";

export default function App() {
  useTheme(); // aplica dark/light no <html>
  return (
    <BrowserRouter>
      <AppRoutes />
    </BrowserRouter>
  );
}