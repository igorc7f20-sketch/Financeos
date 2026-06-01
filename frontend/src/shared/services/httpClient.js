/**
 * HTTP Client - Service Layer
 * 
 * Single Axios instance shared across all features.
 * Handles token injection and automatic refresh on 401.
 */
import axios from 'axios';

const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

const http = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// --Request interceptor - inject access token--
http.interceptors.request.use((config) => {
    const token = localStorage.getItem('access_token');
    if (token) config.headers['Authorization'] = `Bearer ${token}`;
    return config;
});

// --Response interceptor - handle 401 and token refresh--
http.interceptors.response.use(
    (res) => res,
    async (err) => {
        const original = err.config;

        if (err.response?.status === 401 && !original._retry) {
            original._retry = true;

            try {
                const refresh = localStorage.getItem('refresh_token');
                const { data } = await axios.post(`${BASE_URL}/auth/refresh/`, { 
                    refresh,
                });

                localStorage.setItem('accessToken', data.access);
                original.headers['Authorization'] = `Bearer ${data.access}`;
                return http(original);
            } catch {
                localStorage.removeItem('accessToken');
                localStorage.removeItem('refresh_token');
                window.location.href = '/login';
            }
        }

        return Promise.reject(err);
    }
);

export default http;
