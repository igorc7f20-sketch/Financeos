/**
 * Auth Store - Zustand
 * 
 * Global authentication state.
 * Persists tokens in localStorage.
 */
import { create } from "zustand";
import { authApi } from "@/features/auth/api/authApi";

const readStorageItem = (key) => {
    if (typeof window === "undefined") return null;
    return window.localStorage.getItem(key);
};

const writeStorageItem = (key, value) => {
    if (typeof window === "undefined") return;
    window.localStorage.setItem(key, value);
};

const clearStoredTokens = () => {
    if (typeof window === "undefined") return;
    window.localStorage.removeItem("access_token");
    window.localStorage.removeItem("refresh_token");
    window.localStorage.removeItem("accessToken");
    window.localStorage.removeItem("refreshToken");
};

const getStoredAccessToken = () => readStorageItem("access_token") || readStorageItem("accessToken");

export const useAuthStore = create((set) => ({
    user: null,
    isAuthenticated: !!getStoredAccessToken(),

    login: (tokens, user) => {
        writeStorageItem("access_token", tokens.access);
        writeStorageItem("refresh_token", tokens.refresh);
        writeStorageItem("accessToken", tokens.access);
        writeStorageItem("refreshToken", tokens.refresh);
        set({ user: user ?? null, isAuthenticated: true });
    },

    logout: () => {
        clearStoredTokens();
        set({ user: null, isAuthenticated: false });
    },

    setUser: (user) => set({ user }),

    initializeAuth: async () => {
        const accessToken = getStoredAccessToken();

        if (!accessToken) {
            clearStoredTokens();
            set({ user: null, isAuthenticated: false });
            return false;
        }

        try {
            const { data } = await authApi.profile();
            set({ user: data, isAuthenticated: true });
            return true;
        } catch {
            clearStoredTokens();
            set({ user: null, isAuthenticated: false });
            return false;
        }
    },
}));