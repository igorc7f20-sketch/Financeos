import { useNavigate } from "react-router-dom";
import { useAuthStore } from "@/shared/store/authStore";
import { useAuth } from "@/features/auth/hooks/useAuth";
import { useTheme } from "@/shared/hooks/useTheme";
import { useDashboard } from "../hooks/useDashboard";
import MonthlyChart from "../components/MonthlyChart";

const fmt = (value) =>
  new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(value);

export default function DashboardPage() {
  const { user } = useAuthStore();
  const { handleLogout } = useAuth();
  const { theme, toggle } = useTheme();
  const { currentBalance, periodSummary, incomeSeries, expenseSeries, loading } = useDashboard();
  const navigate = useNavigate();

  const periods = [
    { key: "today", label: "Hoje" },
    { key: "week", label: "Esta semana" },
    { key: "month", label: "Este mês" },
  ];

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b border-border bg-card px-6 py-4">
        <div className="max-w-5xl mx-auto flex items-center justify-between">
          <h1 className="text-lg font-bold text-foreground">Rainha Modas</h1>
          <div className="flex items-center gap-4">
            <button onClick={toggle} className="text-sm text-muted-foreground hover:text-foreground transition-colors">
              {theme === "dark" ? "☀️ Claro" : "🌙 Escuro"}
            </button>
            <span className="text-sm text-muted-foreground">{user?.email}</span>
            <button onClick={handleLogout} className="text-sm text-destructive hover:opacity-80 transition-opacity">
              Sair
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-6 py-8">

        <div className="mb-8">
          <h2 className="text-2xl font-bold text-foreground">
            Olá, {user?.full_name?.split(" ")[0] || "usuário"} 👋
          </h2>
          <p className="text-muted-foreground mt-1">Aqui está o resumo do seu caixa.</p>
        </div>

        {/* Saldo atual */}
        <div className="bg-card border border-border rounded-xl p-5 mb-6">
          <p className="text-sm text-muted-foreground mb-1">Saldo atual</p>
          <p className={`text-3xl font-bold ${currentBalance >= 0 ? "text-foreground" : "text-red-500"}`}>
            {loading ? "..." : fmt(currentBalance)}
          </p>
        </div>

        {/* Resumo por período */}
        <div className="bg-card border border-border rounded-xl p-5 mb-8">
          <h3 className="text-sm font-semibold text-foreground mb-4">Resumo por período</h3>
          <div className="grid grid-cols-3 gap-4">
            {periods.map(({ key, label }) => (
              <div key={key}>
                <p className="text-xs text-muted-foreground mb-2">{label}</p>
                <p className="text-sm font-semibold text-green-500">
                  +{loading ? "..." : fmt(periodSummary[key].income)}
                </p>
                <p className="text-sm font-semibold text-red-500">
                  -{loading ? "..." : fmt(periodSummary[key].expense)}
                </p>
              </div>
            ))}
          </div>
        </div>

        {/* Gráficos anuais */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
          <MonthlyChart title="Entradas — últimos 12 meses" data={incomeSeries} color="#22c55e" />
          <MonthlyChart title="Saídas — últimos 12 meses" data={expenseSeries} color="#ef4444" />
        </div>

        {/* Go to Cash */}
        <div className="bg-card border border-border rounded-xl p-6 flex items-center justify-between">
          <div>
            <h3 className="text-base font-semibold text-foreground">Controle de Caixa</h3>
            <p className="text-sm text-muted-foreground mt-1">Registre entradas e saídas em tempo real.</p>
          </div>
          <button
            onClick={() => navigate("/cash")}
            className="px-5 py-2 bg-foreground text-background rounded-lg text-sm font-semibold hover:opacity-90 transition-opacity"
          >
            Abrir Caixa →
          </button>
        </div>

      </main>
    </div>
  );
}