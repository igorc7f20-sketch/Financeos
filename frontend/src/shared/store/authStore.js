/**
 * Auth Store - Zustand
 * 
 * Global authentication state.
 * Persists tokens in localStorage.
 */
import { create } from "zustand";

export const useAuthStore = create((set) => ({
    user: null,
    isAuthenticated: !!localStorage.getItem("access_token"),

    login: (tokens, user) => {
        localStorage.setItem("access_token", tokens.access);
        localStorage.setItem("refresh_token", tokens.refresh);
        set({ user, isAuthenticated: true });
    }

    logout: () => {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        set({ user: null, isAuthenticated: false });
    },

    setUser: (user) => set({ user }),
}));