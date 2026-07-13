import { useState, useEffect } from "react";
import { cashApi } from "@/features/cash/api/cashApi";
import { dashboardApi } from "../api/dashboardApi";

const emptyTotals = { income: 0, expense: 0 };

export function useDashboard() {
    const [currentBalance, setCurrentBalance] = useState(0);
    const [periodSummary, setPeriodSummary] = useState({
        today: emptyTotals, week: emptyTotals, month: emptyTotals,
    });
    const [incomeSeries, setIncomeSeries] = useState([]);
    const [expenseSeries, setExpenseSeries] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function fetchAll() {
            try {
                const [statusRes, summaryRes, incomeRes, expenseRes] = await Promise.all([
                    cashApi.getStatus(),
                    dashboardApi.getPeriodSummary(),
                    dashboardApi.getMonthlyIncome(),
                    dashboardApi.getMonthlyExpense(),
                ]);

                setCurrentBalance(parseFloat(statusRes.data.current_balance));

                const toNum = (t) => ({ income: parseFloat(t.income), expense: parseFloat(t.expense) });
                setPeriodSummary({
                    today: toNum(summaryRes.data.today),
                    week: toNum(summaryRes.data.week),
                    month: toNum(summaryRes.data.month),
                });

                setIncomeSeries(incomeRes.data.map((p) => ({ month: p.month, value: parseFloat(p.value) })));
                setExpenseSeries(expenseRes.data.map((p) => ({ month: p.month, value: parseFloat(p.value) })));
            } catch {
                // dashboard shows zeros on failure
            } finally {
                setLoading(false);
            }
        }
        fetchAll();
    }, []);

    return { currentBalance, periodSummary, incomeSeries, expenseSeries, loading };
}