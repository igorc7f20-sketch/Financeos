/**
 * CashPage — Page Layer
 * Cash register MVP. Matches the Lovable design reference.
 */
import { useState } from "react";
import { useCash } from "../hooks/useCash";

const fmt = (value) =>
  new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
  }).format(value);

export default function CashPage() {
  const {
    transactions,
    loading,
    error,
    filter,
    setFilter,
    addTransaction,
    totalIncome,
    totalExpense,
    balance,
  } = useCash();

  const [form, setForm] = useState({
    type: "income",
    description: "",
    amount: "",
  });
  const [adding, setAdding] = useState(false);

  const onChange = (e) =>
    setForm((f) => ({ ...f, [e.target.name]: e.target.value }));

  const onSubmit = async () => {
    setAdding(true);
    const ok = await addTransaction(form);
    if (ok) setForm((f) => ({ ...f, description: "", amount: "" }));
    setAdding(false);
  };

  const handleCardClick = (type) => {
    setFilter(filter === type ? null : type);
  };

  return (
    <div className="min-h-screen bg-background px-4 py-8">
      <div className="max-w-3xl mx-auto">

        {/* Header */}
        <div className="mb-6">
          <div className="flex items-center gap-2 text-muted-foreground text-xs font-semibold uppercase tracking-widest mb-2">
            <span>🗂</span>
            <span>Controle de Caixa</span>
          </div>
          <h1 className="text-3xl font-bold text-foreground">
            Entradas e saídas
          </h1>
          <p className="text-muted-foreground mt-1">
            Registre movimentações e acompanhe o saldo do seu caixa em tempo real.
          </p>
        </div>

        {/* Summary Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">

          {/* Income */}
          <button
            onClick={() => handleCardClick("income")}
            className={`text-left bg-card border rounded-xl p-5 transition-all hover:shadow-md ${
              filter === "income"
                ? "border-green-500 ring-2 ring-green-200"
                : "border-border"
            }`}
          >
            <div className="flex items-center gap-2 mb-3">
              <span className="text-green-500">⊕</span>
              <span className="text-sm font-medium text-foreground">Entradas</span>
            </div>
            <p className="text-2xl font-bold text-green-500">{fmt(totalIncome)}</p>
          </button>

          {/* Expense */}
          <button
            onClick={() => handleCardClick("expense")}
            className={`text-left bg-card border rounded-xl p-5 transition-all hover:shadow-md ${
              filter === "expense"
                ? "border-red-500 ring-2 ring-red-200"
                : "border-border"
            }`}
          >
            <div className="flex items-center gap-2 mb-3">
              <span className="text-red-500">⊖</span>
              <span className="text-sm font-medium text-foreground">Saídas</span>
            </div>
            <p className="text-2xl font-bold text-red-500">{fmt(totalExpense)}</p>
          </button>

          {/* Balance */}
          <div className="bg-card border border-border rounded-xl p-5">
            <div className="flex items-center gap-2 mb-3">
              <span className="text-foreground">◎</span>
              <span className="text-sm font-medium text-foreground">Saldo</span>
            </div>
            <p className={`text-2xl font-bold ${
              balance >= 0 ? "text-foreground" : "text-red-500"
            }`}>
              {fmt(balance)}
            </p>
          </div>

        </div>

        {/* New Transaction Form */}
        <div className="bg-card border border-border rounded-xl p-5 mb-6">
          <h2 className="text-base font-semibold text-foreground mb-4">
            Nova movimentação
          </h2>
          <div className="flex flex-col sm:flex-row gap-3">
            <select
              name="type"
              value={form.type}
              onChange={onChange}
              className="px-3 py-2 rounded-lg border border-input bg-background
                         text-foreground text-sm focus:outline-none focus:ring-2 focus:ring-ring"
            >
              <option value="income">Entrada</option>
              <option value="expense">Saída</option>
            </select>

            <input
              name="description"
              value={form.description}
              onChange={onChange}
              placeholder="Descrição (ex.: Venda à vista)"
              className="flex-1 px-3 py-2 rounded-lg border border-input bg-background
                         text-foreground text-sm placeholder:text-muted-foreground
                         focus:outline-none focus:ring-2 focus:ring-ring"
            />

            <input
              name="amount"
              type="number"
              min="0"
              step="0.01"
              value={form.amount}
              onChange={onChange}
              placeholder="0,00"
              className="w-32 px-3 py-2 rounded-lg border border-input bg-background
                         text-foreground text-sm placeholder:text-muted-foreground
                         focus:outline-none focus:ring-2 focus:ring-ring"
            />

            <button
              onClick={onSubmit}
              disabled={adding || !form.description || !form.amount}
              className="px-5 py-2 bg-foreground text-background rounded-lg text-sm
                         font-semibold hover:opacity-90 disabled:opacity-40 transition-opacity"
            >
              {adding ? "..." : "Adicionar"}
            </button>
          </div>
          {error && (
            <p className="text-sm text-red-500 mt-2">{error}</p>
          )}
        </div>

        {/* Transaction List */}
        <div className="bg-card border border-border rounded-xl p-5">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-base font-semibold text-foreground">
              Movimentações
              {filter && (
                <span className="ml-2 text-xs font-normal text-muted-foreground">
                  ({filter === "income" ? "entradas" : "saídas"})
                </span>
              )}
            </h2>
            {filter && (
              <button
                onClick={() => setFilter(null)}
                className="text-xs text-muted-foreground hover:text-foreground transition-colors"
              >
                Limpar filtro ✕
              </button>
            )}
          </div>

          {loading ? (
            <p className="text-center text-muted-foreground text-sm py-8">
              Carregando...
            </p>
          ) : transactions.length === 0 ? (
            <p className="text-center text-muted-foreground text-sm py-8">
              Nenhuma movimentação registrada ainda.
            </p>
          ) : (
            <ul className="divide-y divide-border">
              {transactions.map((t) => (
                <li key={t.id} className="flex items-center justify-between py-3">
                  <div>
                    <p className="text-sm font-medium text-foreground">{t.title}</p>
                    <p className="text-xs text-muted-foreground">{t.date}</p>
                  </div>
                  <span className={`text-sm font-semibold ${
                    t.type === "income" ? "text-green-500" : "text-red-500"
                  }`}>
                    {t.type === "income" ? "+" : "-"}{fmt(parseFloat(t.amount))}
                  </span>
                </li>
              ))}
            </ul>
          )}
        </div>

      </div>
    </div>
  );
}