/**
 * 
 * Manage login and register state.
 * Calls the API layer, updates the auth store.
*/
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { authApi } from "../api/authApi";
import { useAuthStore } from "@/shared/store/authStore";

export function useAuth() {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const navigate = useNavigate();
    const { login, logout } = useAuthStore();

    const handleLogin = async ({ email, password }) => {
        setLoading(true);
        setError(null);

        try {
            const loginResponse = await authApi.login({ 
                email: email.trim(),
                password, 
            });

            const { access, refresh } = loginResponse.data;

            if (!access || !refresh) {
                throw new Error("Tokens não retornados pelo servidor.");
            }

            // Salva os tokens antes de consultar o perfil.
            login({ access, refresh }, null);

            const profileResponse = await authApi.profile();
            const user = profileResponse.data;

            // Atualiza o estado incluindo o usuário.
            login({ access, refresh }, user);

            navigate("/dashboard", { replace: true });

            return true;
        } catch (err) {
            console.error(
                "Login error:",
                 err.response?.data || err.message || err
            );

            // Limpa um possível estado parcial de autenticação.
            logout();

            const status = err.response?.status;
            
            if (status === 401 || status === 400) {
                setError("E-mail ou senha inválidos");
            } else if (!err.response) {
                setError(
                    "Não foi possível conectar ao servidor."
                );
            } else {
                setError("Não foi possível realizar o login");
            }

            return false;
        } finally {
            setLoading(false);
        }
    };

    const handleRegister = async ({ email, full_name, password }) => {
        setLoading(true);
        setError(null);
        try {
            await authApi.register({ email, full_name, password });
            await handleLogin({ email, password });
        } catch (err) {
            console.error("Register error:", err);
            setError("Erro ao criar conta. Tente novamente.");
        } finally {
            setLoading(false);
        }
    };

    const handleLogout = () => {
        logout();
        navigate("/login");
    };

    return {
        loading,
        error,
        handleLogin,
        handleRegister,
        handleLogout,
    };
}