/**
 * useDashboard - Hook Layer
 * Fetches summary data from the transactions API.
 */
import { useState, useEffect } from 'react';
import { cashApi } from '@/features/cash/api/cashApi';

export function useDashboard() {
    const [summary, setSummary] = useState({
        totalIncome: 0,
        totalExpense: 0,
        Balance: 0,
    });
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function fetchSummary() {
            try {
                const { data } = await cashApi.listTransactions({});
                const transactions = Array.isArray(data) ? data : data.results || [];

                const totalIncome = transactions
                    .filter((t) => t.type === 'income')
                    .reduce((acc, t) => acc + parseFloat(t.amount), 0);

                const totalExpense = transactions
                    .filter((t) => t.type === 'expense')
                    .reduce((acc, t) => acc + parseFloat(t.amount), 0);

                setSummary({
                    totalIncome,
                    totalExpense,
                    Balance: totalIncome - totalExpense,
                });
            } catch {
                // silently fail - dashboard shows zeros
            } finally {
                setLoading(false);
            }
        }

        fetchSummary();
    }, []);

    return { summary, loading };
}
