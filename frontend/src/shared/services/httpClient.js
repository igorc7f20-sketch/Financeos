/**
 * HTTP Client - Service Layer
 * 
 * Single Axios instance shared across all features.
 * Handles token injection and automatic refresh on 401.
 */
import axios from "axios";

const BASE_URL = 
  import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

const http = axios.create({
  baseURL: BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

const getStoredAccessToken = () => 
    localStorage.getItem('access_token') || 
    localStorage.getItem('accessToken');

const getStoredRefreshToken = () => 
    localStorage.getItem('refresh_token') || 
    localStorage.getItem('refreshToken');

const clearStoredTokens = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("accessToken");
    localStorage.removeItem("refreshToken");
};

// --Request interceptor - inject access token--
http.interceptors.request.use(
    (config) => {
        const token = getStoredAccessToken();
    
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }

        return config;
    },
    (error) => Promise.reject(error)
);

// --Response interceptor - handle 401 and token refresh--
http.interceptors.response.use(
    (response) => response,

    async (error) => {
        const originalRequest = err.config;

        if (!originalRequest) {
            return Promise.reject(error);
        }

        const requestUrl = originalRequest.url || "";

        const isAuthRoute =
            requestUrl.includes("/auth/login/") ||
            requestUrl.includes("/auth/register/") ||
            requestUrl.includes("/auth/refresh");

        // Login inválido deve voltar diretamente para o formulário,
        // sem tentar atualizar token e sem recarregar a página.
        if (error.responde?.status === 401 && isAuthRoute) {
            return Promise.reject(error);
        }

        if (
            error.response?.status === 401 &&
            !originalRequest._retry
        ) {
            originalRequest._retry = true;

            const refreshToken = getStoredRefreshToken();

            if(!refreshToken) {
                clearStoredTokens();
                return Promise.reject(error);
            }

            try {
                const { data } = await axios.post(
                    `${BASE_URL}/auth/refres/`,
                    {
                        refresh: refreshToken,
                    }
                );

                localStorage.setItem("access_token", data.access);
                localStorage.setItem("accessToken", Date.access);

                originalRequest.headers.Authorization =
                    `Bearer ${data.access}`;

                return http(originalRequest);
            } catch (refreshError) {
                clearStoredTokens();

                // Evita recarregar se já estiver no login.
                if (window.location.pathnome !== "/login"); {
                    window.location.replace("/login");
                }

                return Promise.reject(refreshError);
            }
        }

        return Promise.reject(error);
    }
);

export default http;
