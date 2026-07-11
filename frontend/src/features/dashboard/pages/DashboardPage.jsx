/**
 * DashboardPage — Page Layer
 * Main screen after login. Shows real cash summary from API.
 */
import { useNavigate } from "react-router-dom";
import { useAuthStore } from "@/shared/store/authStore";
import { useAuth } from "@/features/auth/hooks/useAuth";
import { useTheme } from "@/shared/hooks/useTheme";
import { useDashboard } from "../hooks/useDashboard";

const fmt = (value) =>
  new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
  }).format(value);

export default function DashboardPage() {
  const { user } = useAuthStore();
  const { handleLogout } = useAuth();
  const { theme, toggle } = useTheme();
  const { summary, loading } = useDashboard();
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-background">

      {/* Header */}
      <header className="border-b border-border bg-card px-6 py-4">
        <div className="max-w-5xl mx-auto flex items-center justify-between">
          <h1 className="text-lg font-bold text-foreground">Rainha Modas</h1>
          <div className="flex items-center gap-4">
            <button
              onClick={toggle}
              className="text-sm text-muted-foreground hover:text-foreground transition-colors"
            >
              {theme === "dark" ? "☀️ Claro" : "🌙 Escuro"}
            </button>
            <span className="text-sm text-muted-foreground">{user?.email}</span>
            <button
              onClick={handleLogout}
              className="text-sm text-destructive hover:opacity-80 transition-opacity"
            >
              Sair
            </button>
          </div>
        </div>
      </header>

      {/* Content */}
      <main className="max-w-5xl mx-auto px-6 py-8">

        {/* Welcome */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-foreground">
            Olá, {user?.full_name?.split(" ")[0] || "usuário"} 👋
          </h2>
          <p className="text-muted-foreground mt-1">
            Aqui está o resumo do seu caixa hoje.
          </p>
        </div>

        {/* Summary Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
          <div className="bg-card border border-border rounded-xl p-5">
            <p className="text-sm text-muted-foreground mb-1">Entradas</p>
            <p className="text-2xl font-bold text-green-500">
              {loading ? "..." : fmt(summary.totalIncome)}
            </p>
          </div>
          <div className="bg-card border border-border rounded-xl p-5">
            <p className="text-sm text-muted-foreground mb-1">Saídas</p>
            <p className="text-2xl font-bold text-red-500">
              {loading ? "..." : fmt(summary.totalExpense)}
            </p>
          </div>
          <div className="bg-card border border-border rounded-xl p-5">
            <p className="text-sm text-muted-foreground mb-1">Saldo atual</p>
            <p className={`text-2xl font-bold ${
              summary.balance >= 0 ? "text-foreground" : "text-red-500"
            }`}>
              {loading ? "..." : fmt(summary.balance)}
            </p>
          </div>
        </div>

        {/* Go to Cash */}
        <div className="bg-card border border-border rounded-xl p-6 flex items-center justify-between">
          <div>
            <h3 className="text-base font-semibold text-foreground">
              Controle de Caixa
            </h3>
            <p className="text-sm text-muted-foreground mt-1">
              Registre entradas e saídas em tempo real.
            </p>
          </div>
          <button
            onClick={() => navigate("/cash")}
            className="px-5 py-2 bg-foreground text-background rounded-lg
                       text-sm font-semibold hover:opacity-90 transition-opacity"
          >
            Abrir Caixa →
          </button>
        </div>

      </main>
    </div>
  );
}