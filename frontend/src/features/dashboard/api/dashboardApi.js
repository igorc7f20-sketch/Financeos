import http from "@/shared/services/httpClient";

export const dashboardApi = {
    getMonthlyIncome: () => http.get("/dashboard/monthly-income/"),
    getMonthlyExpense: () => http.get("/dashboard/monthly-expense/"),
    getPeriodSummary: (params = {}) => http.get("/dashboard/period-summary/"),
};