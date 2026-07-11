/**
 * useCash - Hook Layer
 * Manages cash register state and business logic.
 * Calls API layer, exposes data and actions to the page.
 */
import { useState, useEffect, useCallback } from "react";
import { cashApi } from "../api/cashApi";

function formatDate(date) {
    return date.toISOString().split("T")[0]; // YYYY-MM-DD
}

function getDefaultPeriod() {
    const today = new Date();
    const firstDayOfMonth = new Date(today.getFullYear(), today.getMonth(), 1);
    return {
        dateFrom: formatDate(firstDayOfMonth),
        dateTo: formatDate(today),
    };
}

export function useCash() {
    const defaultPeriod = getDefaultPeriod();

    // Inputs Shown in the date pickers
    const [dateFrom, setDateFrom] = useState(defaultPeriod.dateFrom);
    const [dateTo, setDateTo] = useState(defaultPeriod.dateTo);

    // Period actually applied to the query (only changes on "Filtrar")
    const [appliedPeriod, setAppliedPeriod] = useState(defaultPeriod);

    const [movements, setMovements] = useState([]);
    const [totals, setTotals] = useState({ income: 0, expense: 0, });
    const [currentBalance, setCurrentBalance] = useState(0);

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    
    const fetchStatus = useCallback(async () => {
        try {
            const { data } = await cashApi.getStatus();
            setCurrentBalance(parseFloat(data.current_balance || 0));
        } catch {
            // Status is secondary; a failure here shouldn't block the list.
        }
    }, []);

    const fetchMovements = useCallback(async () => {
        setLoading(true);
        setError(null);
        try {
            const params = {
                date_from: appliedPeriod.dateFrom,
                date_to: appliedPeriod.dateTo,
            };
            const { data } = await cashApi.listTransactions(params);
            setMovements(data.results || []);
            if (data.totals) {
                setTotals({
                    income: parseFloat(data.totals.income),
                    expense: parseFloat(data.totals.expense),
                });
            }
        } catch {
            setError("Erro ao carregar movimentações. Tente novamente.");
        } finally {
            setLoading(false);
        }
    }, [appliedPeriod]);

    useEffect(() => {
        fetchStatus();
        fetchMovements();
    }, [fetchStatus, fetchMovements]);

    function applyPeriodFilter() {
        if (!dateFrom || !dateTo) {
            setError("Informe a data inicial e a data final.");
            return;
        }
        if (dateFrom > dateTo) {
            setError("A data inicial não pode ser posterior à data final.");
            return;
        }
        setAppliedPeriod({ dateFrom, dateTo });
    }

    const addMovement = async ({ type, description, amount }) => {
        if (!description.trim() || !amount || parseFloat(amount) <= 0) return false;
        try {
            await cashApi.createTransaction({
                type,
                description,
                amount: parseFloat(amount),
            });
            await Promise.all([fetchMovements(), fetchStatus()]);
            return true;
        } catch {
            setError("Erro ao adicionar movimentação. Tente novamente.");
            return false;
        }
    };

    return {
        movements,
        loading,
        error,
        dateFrom,
        dateTo,
        setDateFrom,
        setDateTo,
        applyPeriodFilter,
        addMovement,
        totalIncome: totals.income,
        totalExpense: totals.expense,
        currentBalance,
    };
}