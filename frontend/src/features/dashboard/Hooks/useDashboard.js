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
            const [statusRes, summaryRes, incomeRes, expenseRes] = await Promise.allSettled([
                cashApi.getStatus(),
                dashboardApi.getPeriodSummary(),
                dashboardApi.getMonthlyIncome(),
                dashboardApi.getMonthlyExpense(),
            ]);

            if (statusRes.status === "fulfilled") {
                setCurrentBalance(parseFloat(statusRes.value.data.current_balance));
            }

            if (summaryRes.status === "fulfilled") {
                const toNum = (t) => ({ income: parseFloat(t.income), expense: parseFloat(t.expense) });
                const d = summaryRes.value.data;
                setPeriodSummary({ today: toNum(d.today), week: toNum(d.week), month: toNum(d.month) });
            }

            if (incomeRes.status === "fulfilled") {
                setIncomeSeries(incomeRes.value.data.map((p) => ({ month: p.month, value: parseFloat(p.value) })));
            }

            if (expenseRes.status === "fulfilled") {
                setExpenseSeries(expenseRes.value.data.map((p) => ({ month: p.month, value: parseFloat(p.value) })));
            }

            setLoading(false);    
        }
        fetchAll();
    }, []);

    return { currentBalance, periodSummary, incomeSeries, expenseSeries, loading };
}