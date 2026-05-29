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
    const { login } = useAuthStore();

    const handleLogin = async ({ email, password }) => {
        setLoading(true);
        setError(null);
        try {
            const loginResponse = await authApi.login({ email, password });
            console.log("LOGIN RESPONSE:", loginResponse);
            console.log("LOGIN DATA:", loginResponse.data);

            const tokens = loginResponse.data;
            console.log("ACCESS TOKEN:", tokens.access);
            console.log("REFRESH TOKEN:", tokens.refresh);

            login(tokens, null);
            navigate("/dashboard");
        } catch (err) {
            console.error("Login error:", err);
            setError("E-mail ou senha inválidas. Tente novamente.");
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
        LogOut();
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