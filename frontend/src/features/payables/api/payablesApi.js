/**
 *  Payables API - API Layer
 *  Only HTTP calls. No state, no logic.
 */
import http from "@/shared/services/httpClient";

export const payablesApi = {
    getSummary: () => http.get("/payables/summary/"),

    listInstallments: (params = {}) =>
        http.get("/payables/", { params }),

    createPayable: (data) =>
        http.post("/payables/", data),

    markAsPaid: (installmentId) =>
        http.post(`/payables/installments/${installmentId}/play/`),
}