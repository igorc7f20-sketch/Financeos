/**
 * RegisterPage- Page Layer
 * Simple register form. Delefates logic to useAuth hook.
 */
import { useState } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

export default function RegisterPage() {
    const [form, setForm] = useState({ email: "", full_name: "", password: "" });
    const { loading, error, handleRegister } = useAuth();

    const onChange = (e) =>
        setForm((f) => ({ ...f, [e.target.name]: e.target.value }));

    const onSubmit = (e) => {
        e.preventDefault();
        handleRegister(form);
    };

    return (
    <div className="min-h-screen flex items-center justify-center bg-background px-4">
      <div className="w-full max-w-sm">

        <div className="mb-8 text-center">
          <h1 className="text-2xl font-bold text-foreground">FinanceOS</h1>
          <p className="text-sm text-muted-foreground mt-1">Crie sua conta</p>
        </div>

        <div className="bg-card border border-border rounded-lg p-6 shadow-sm">
          {error && (
            <p className="text-sm text-destructive mb-4 text-center">{error}</p>
          )}

          <form onSubmit={onSubmit} className="space-y-4">
            <div>
              <label className="text-sm font-medium text-foreground block mb-1">
                Nome completo
              </label>
              <input
                name="full_name"
                type="text"
                required
                value={form.full_name}
                onChange={onChange}
                placeholder="Seu nome"
                className="w-full px-3 py-2 rounded-md border border-input bg-background
                           text-foreground text-sm placeholder:text-muted-foreground
                           focus:outline-none focus:ring-2 focus:ring-ring"
              />
            </div>

            <div>
              <label className="text-sm font-medium text-foreground block mb-1">
                E-mail
              </label>
              <input
                name="email"
                type="email"
                required
                value={form.email}
                onChange={onChange}
                placeholder="seu@email.com"
                className="w-full px-3 py-2 rounded-md border border-input bg-background
                           text-foreground text-sm placeholder:text-muted-foreground
                           focus:outline-none focus:ring-2 focus:ring-ring"
              />
            </div>

            <div>
              <label className="text-sm font-medium text-foreground block mb-1">
                Senha
              </label>
              <input
                name="password"
                type="password"
                required
                value={form.password}
                onChange={onChange}
                placeholder="••••••••"
                className="w-full px-3 py-2 rounded-md border border-input bg-background
                           text-foreground text-sm placeholder:text-muted-foreground
                           focus:outline-none focus:ring-2 focus:ring-ring"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-2 px-4 bg-primary text-primary-foreground
                         rounded-md text-sm font-medium hover:opacity-90
                         disabled:opacity-50 transition-opacity"
            >
              {loading ? "Criando conta..." : "Criar conta"}
            </button>
          </form>
        </div>

        <p className="text-center text-sm text-muted-foreground mt-4">
          Já tem conta?{" "}
          <Link to="/login" className="text-primary hover:underline">
            Entrar
          </Link>
        </p>

      </div>
    </div>
  );
}