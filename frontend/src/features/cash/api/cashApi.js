/**
 * Cash API - API Layer
 * Only HTTP calls. No state, no logic.
 */
import http from "@/shared/services/httpClient";

export const cashApi = {
    listTransactions: (params = {}) =>
        http.get("/transactions/", { params }),

    createTransaction: (data) =>
        http.post("/transactions/", data),
};