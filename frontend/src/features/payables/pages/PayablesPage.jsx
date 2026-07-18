import { useState } from "react";
import { usePayables } from "../hooks/usePayables";

const fmt = (value) =>
  new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(value);

const STATUS_TABS = [
  { value: "pending", label: "Pendentes" },
  { value: "paid", label: "Pagas" },
  { value: "all", label: "Todas" },
];

export default function PayablesPage() {
  const {
    installments, summary, loading, error,
    statusFilter, setStatusFilter,
    createPayable, payInstallment,
  } = usePayables();

  const [form, setForm] = useState({
    description: "",
    totalAmount: "",
    installmentsCount: 1,
    firstDueDate: "",
  });
  const [creating, setCreating] = useState(false);

  const onChange = (e) => setForm((f) => ({ ...f, [e.target.name]: e.target.value }));

  const onSubmit = async () => {
    setCreating(true);
    const ok = await createPayable(form);
    if (ok) {
      setForm({ description: "", totalAmount: "", installmentsCount: 1, firstDueDate: "" });
    }
    setCreating(false);
  };

  const statusBadge = (installment) => {
    if (installment.status === "paid") {
      return <span className="text-xs font-semibold text-green-500">Pago</span>;
    }
    if (installment.is_overdue) {
      return <span className="text-xs font-semibold text-red-500">Atrasado</span>;
    }
    return <span className="text-xs font-semibold text-muted-foreground">Pendente</span>;
  };

  return (
    <div className="px-4 py-8">
      <div className="max-w-3xl mx-auto">

        <div className="mb-6">
          <div className="flex items-center gap-2 text-muted-foreground text-xs font-semibold uppercase tracking-widest mb-2">
            <span>📄</span>
            <span>Financeiro</span>
          </div>
          <h1 className="text-3xl font-bold text-foreground">Contas a pagar</h1>
          <p className="text-muted-foreground mt-1">
            Cadastre contas avulsas ou parceladas e acompanhe os vencimentos.
          </p>
        </div>

        {/* Summary Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">
          <div className="bg-card border border-border rounded-xl p-5">
            <p className="text-sm font-medium text-foreground mb-2">Atrasado</p>
            <p className="text-2xl font-bold text-red-500">{fmt(summary.overdue_total)}</p>
            <p className="text-xs text-muted-foreground mt-1">
              {summary.overdue_count} {summary.overdue_count === 1 ? "conta" : "contas"}
            </p>
          </div>
          <div className="bg-card border border-border rounded-xl p-5">
            <p className="text-sm font-medium text-foreground mb-2">A vencer este mês</p>
            <p className="text-2xl font-bold text-foreground">{fmt(summary.this_month_total)}</p>
            <p className="text-xs text-muted-foreground mt-1">
              {summary.this_month_count} {summary.this_month_count === 1 ? "conta" : "contas"}
            </p>
          </div>
        </div>

        {/* New Payable Form */}
        <div className="bg-card border border-border rounded-xl p-5 mb-6">
          <h2 className="text-base font-semibold text-foreground mb-4">Nova conta</h2>
          <div className="flex flex-col sm:flex-row gap-3">
            <input
              name="description"
              value={form.description}
              onChange={onChange}
              placeholder="Descrição (ex.: Aluguel, Fornecedor X)"
              className="flex-1 px-3 py-2 rounded-lg border border-input bg-background
                         text-foreground text-sm placeholder:text-muted-foreground
                         focus:outline-none focus:ring-2 focus:ring-ring"
            />
            <input
              name="totalAmount"
              type="number"
              min="0"
              step="0.01"
              value={form.totalAmount}
              onChange={onChange}
              placeholder="Valor total"
              className="w-32 px-3 py-2 rounded-lg border border-input bg-background
                         text-foreground text-sm placeholder:text-muted-foreground
                         focus:outline-none focus:ring-2 focus:ring-ring"
            />
            <input
              name="installmentsCount"
              type="number"
              min="1"
              value={form.installmentsCount}
              onChange={onChange}
              placeholder="Parcelas"
              className="w-24 px-3 py-2 rounded-lg border border-input bg-background
                         text-foreground text-sm placeholder:text-muted-foreground
                         focus:outline-none focus:ring-2 focus:ring-ring"
            />
            <input
              name="firstDueDate"
              type="date"
              value={form.firstDueDate}
              onChange={onChange}
              className="px-3 py-2 rounded-lg border border-input bg-background
                         text-foreground text-sm focus:outline-none focus:ring-2 focus:ring-ring"
            />
            <button
              onClick={onSubmit}
              disabled={creating || !form.description || !form.totalAmount || !form.firstDueDate}
              className="px-5 py-2 bg-foreground text-background rounded-lg text-sm
                         font-semibold hover:opacity-90 disabled:opacity-40 transition-opacity"
            >
              {creating ? "..." : "Adicionar"}
            </button>
          </div>
          <p className="text-xs text-muted-foreground mt-2">
            Deixe parcelas em 1 para uma conta avulsa. O valor total é dividido igualmente entre as parcelas.
          </p>
          {error && <p className="text-sm text-red-500 mt-2">{error}</p>}
        </div>

        {/* List */}
        <div className="bg-card border border-border rounded-xl p-5">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-base font-semibold text-foreground">Parcelas</h2>
            <div className="flex gap-1 bg-secondary rounded-lg p-1">
              {STATUS_TABS.map((tab) => (
                <button
                  key={tab.value}
                  onClick={() => setStatusFilter(tab.value)}
                  className={`px-3 py-1 rounded-md text-xs font-medium transition-colors ${
                    statusFilter === tab.value
                      ? "bg-foreground text-background"
                      : "text-muted-foreground hover:text-foreground"
                  }`}
                >
                  {tab.label}
                </button>
              ))}
            </div>
          </div>

          {loading ? (
            <p className="text-center text-muted-foreground text-sm py-8">Carregando...</p>
          ) : installments.length === 0 ? (
            <p className="text-center text-muted-foreground text-sm py-8">Nenhuma conta encontrada.</p>
          ) : (
            <ul className="divide-y divide-border">
              {installments.map((i) => (
                <li key={i.id} className="flex items-center justify-between py-3 gap-3">
                  <div className="min-w-0">
                    <p className="text-sm font-medium text-foreground truncate">
                      {i.description}
                      {i.total_installments > 1 && (
                        <span className="text-muted-foreground font-normal">
                          {" "}({i.installment_number}/{i.total_installments})
                        </span>
                      )}
                    </p>
                    <div className="flex items-center gap-2 mt-0.5">
                      <p className="text-xs text-muted-foreground">Vence em {i.due_date}</p>
                      {statusBadge(i)}
                    </div>
                  </div>
                  <div className="flex items-center gap-3 shrink-0">
                    <span className="text-sm font-semibold text-foreground">{fmt(i.amount)}</span>
                    {i.status === "pending" && (
                      <button
                        onClick={() => payInstallment(i.id)}
                        className="px-3 py-1.5 rounded-lg border border-input text-xs font-medium
                                   text-foreground hover:bg-secondary transition-colors"
                      >
                        Marcar como pago
                      </button>
                    )}
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>

      </div>
    </div>
  );
}