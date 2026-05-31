/**
 * DashboardPage — Page Layer
 * Main screen after login. Simple and functional MVP.
 */
import { useAuthStore } from "@/shared/store/authStore";
import { useAuth } from "@/features/auth/hooks/useAuth";
import { useTheme } from "@/shared/hooks/useTheme";
import { useNavigate } from "react-router-dom";

export default function DashboardPage() {
  const { user } = useAuthStore();
  const { handleLogout } = useAuth();
  const { theme, toggle } = useTheme();
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-background">

      {/* Header */}
      <header className="border-b border-border bg-card px-6 py-4">
        <div className="max-w-5xl mx-auto flex items-center justify-between">
          <h1 className="text-lg font-bold text-foreground">FinanceOS</h1>
          <div className="flex items-center gap-4">
            <button
              onClick={toggle}
              className="text-sm text-muted-foreground hover:text-foreground transition-colors"
            >
              {theme === "dark" ? "☀️ Claro" : "🌙 Escuro"}
            </button>
            <span className="text-sm text-muted-foreground">
              {user?.email}
            </span>
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
            Bem-vindo ao FinanceOS. O caixa está sendo construído.
          </p>
        </div>

        {/* Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
          <div className="bg-card border border-border rounded-lg p-5">
            <p className="text-sm text-muted-foreground">Saldo atual</p>
            <button onClick={() => navigate("/cash")} className="...">Ir para o Caixa →</button>
            <p className="text-2xl font-bold text-foreground mt-1">R$ 0,00</p>
          </div>
          <div className="bg-card border border-border rounded-lg p-5">
            <p className="text-sm text-muted-foreground">Entradas hoje</p>
            <p className="text-2xl font-bold text-foreground mt-1">R$ 0,00</p>
          </div>
          <div className="bg-card border border-border rounded-lg p-5">
            <p className="text-sm text-muted-foreground">Saídas hoje</p>
            <p className="text-2xl font-bold text-foreground mt-1">R$ 0,00</p>
          </div>
        </div>

        {/* Notice */}
        <div className="bg-card border border-border rounded-lg p-6 text-center">
          <p className="text-muted-foreground text-sm">
            🚧 Módulo de caixa em desenvolvimento — em breve você poderá
            registrar entradas, saídas e acompanhar o saldo em tempo real.
          </p>
        </div>

      </main>
    </div>
  );
}