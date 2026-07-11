/**
 * Cash API - API Layer
 * Only HTTP calls. No state, no logic.
 */
import http from "@/shared/services/httpClient";

export const cashApi = {
    getStatus: () => http.get("/cash/status/"),
    
    listTransactions: (params = {}) =>
        http.get("/cash/movements/", { params }),

    createTransaction: (data) =>
        http.post("/cash/movements/", data),
};