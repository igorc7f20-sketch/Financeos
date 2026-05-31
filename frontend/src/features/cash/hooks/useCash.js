/**
 * useCash - Hook Layer
 * Manages cash register state and business logic.
 * Calls API layer, exposes data and actions to the page.
 */
import { useState, useEffect, useCallback } from "react";
import { cashApi } from "../api/cashApi";

export function useCash() {
    const [transactions, setTransactions] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [filters, setFilters] = useState(null); // null | "income" | "expense"

    const fetchTransactions = useCallback(async () => {
        setLoading(true);
        setError(null);
        try {
            const params = filters ? { type: filters } : {};
            const { data } = await cashApi.listTransactions(params);
            setTransactions(data.results || data);
        } catch {
            setError("Erro ao carregar transações. Tente novamente.");
        } finally {
            setLoading(false);
        }
    }, [filters]);

    useEffect(() => {
        fetchTransactions();
    }, [fetchTransactions]);

    const addTransaction = async ({ type, description, amount }) => {
        if (!description.trim() || !amount || parseFloat(amount) <= 0) return false;
        try {
            await cashApi.createTransaction({
                title: description,
                amount: parseFloat(amount),
                type,
                date: new Date().toISOString().split("T")[0],
            });
            await fetchTransactions();
            return true;
        } catch {
            setError("Erro ao adicionar transação. Tente novamente.");
            return false;
        }
    };

    // Totals computed from full list (no filters)
    const [allTransactions, setAllTransactions] = useState([]);

    useEffect(() => {
        cashApi.listTransactions({}).then(({ data}) => {
            setAllTransactions(data.results || data);
        }).catch(() => {});
    }, [transactions]);

    const totalIncome = allTransactions
        .filter((t) => t.type === "income")
        .reduce((acc, t) => acc + parseFloat(t.amount), 0);

    const totalExpense = allTransactions
        .filter((t) => t.type === "expense")
        .reduce((acc, t) => acc + parseFloat(t.amount), 0);

    const balance = totalIncome - totalExpense;

    return {
        transactions,
        loading,
        error,
        filters,
        setFilters,
        addTransaction,
        totalIncome,
        totalExpense,
        balance
    };
}