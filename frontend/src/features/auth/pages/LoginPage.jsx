/**
 * LoginPage - Page Layer
 * 
 * Simple login form.
 * Delegates all logic to useAuth hook. 
 */
import {  useState } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

export default function LoginPage() {
    const [form, setForm] = useState({ email: "", password: "" });
    const { loading, error, handleLogin } = useAuth();

    const onChange = (e) =>
        setForm((f) => ({ ...f, [e.target.name]: e.target.value }));

    const onSubmit = (e) => {
        e.preventDefault();
        handleLogin(form);
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-background px-4">
            <div className="w-full max-w-sm">

                {/* Header */}
                <div className="mb-8 text-center">
                    <h1 className="text-2x1 font-bold text-foreground">Bem-vindo</h1>
                    <p className="text-sm text-muted-foreground mt-1">
                        Entre com sua conta
                    </p>
                </div>

                {/* Card */}
                <div className="bg-card border border-border rounded-lg p-6 shadow-sm">

                    {error && (
                        <p className="text-sm text-destructive mb-4 text-center">{error}</p>
                    )}

                    <form onSubmit={onSubmit} className="space-y-4">
                        <div>
                            <label className="text-sm font-medium text-foreground blockmb-1">
                                Email
                            </label>
                            <input
                                type="email"
                                name="email"
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
                                type="password"
                                name="password"
                                required
                                value={form.password}
                                onChange={onChange}
                                placeholder="Sua senha"
                                className="w-full px-3 py-2 rounded-md border border-input bg-background
                                           text-foreground text-sm placeholder:text-muted-foreground
                                           focus:outline-none focus:ring-2 focus:ring-ring"
                            />
                        </div>

                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full py-2 px-4 bg-primary text-primary-foreground
                                       rounded-md text-sm font-medium-hover:opacity-90
                                       disabled:opacity-50 trasation-opacity"
                        >
                            {loading ? "Entrando..." : "Entrar"}
                        </button>
                    </form>
                </div>

                {/* Footer */}
                <p className="text-center text-sm text-muted-foreground mt-4">
                    Não tem uma conta?{" "}
                    <Link to="/register" className="text-primary hover:underline">
                        Registre-se
                    </Link>
                </p>

            </div>
        </div>
    );
}
    