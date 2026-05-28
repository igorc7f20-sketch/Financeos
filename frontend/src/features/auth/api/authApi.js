/**
 * Auth API - API Layer
 * Only HTTP calls. No state, no logic.
 */
import http from "@/shared/services/httpClient";

export const authApi = {
    login: (credentials) => http.post("/auth/login/", credentials),
    register: (data) => http.post("/auth/register/", data),
    profile: () => http.get("/auth/profile/"),
};