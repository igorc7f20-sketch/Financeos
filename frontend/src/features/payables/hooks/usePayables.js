import { useState, useEffect, useCallback } from "react";
import { payablesApi } from "../api/payablesApi";

export function usePayables() {
    const [installments, setInstallments] = useState([]);
    const [summary, setSummary] = useState({
        overdue_total: 0, overdue_count: 0,
        this_month_total: 0, this_month_count: 0,
    });
    const [statusFilter, setStatusFilter] = useState("pending"); // "pending" | "paid" | "all"
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchSummary = useCallback(async () => {
        try {
            const { data } = await payablesApi.getSummary();
            setSummary({
                overdue_total: parseFloat(data.overdue_total),
                overdue_count: data.overdue_count,
                this_month_total: parseFloat(data.this_month_total),
                this_month_count: data.this_month_count,
            });
        } catch {
            // summary is secondary, don't block the list
        }
    }, []);

    const fetchInstallments = useCallback(async () => {
        setLoading(true);
        setError(null);
        try {
            const params = statusFilter === "all" ? {} : { status: statusFilter };
            const { data } = await payablesApi.listInstallments(params);
            setInstallments(data.results || []);
        } catch {
            setError("Erro ao carregar contas a pagar. Tente novamente");
        } finally {
            setLoading(false);
        }
    }, [statusFilter]);

    useEffect(() => {
        fetchSummary();
        fetchInstallments();
    }, [fetchSummary, fetchInstallments]);

    const createPayable = async ({ description, totalAmount, installmentsCount, firstDueDate }) => {
        if (!description.trim() || !totalAmount ||  parseFloat(totalAmount) <= 0 || !firstDueDate) {
            return false;
        }
        try {
            await payablesApi.createPayable({
                description,
                total_amount: parseFloat(totalAmount),
                installments_count: parseInt(installmentsCount, 10) || 1,
                fist_due_date: firstDueDate,
            });
            await Promise.all([fetchInstallments(), fetchSummary()]);
            return true;
        } catch {
            setError("Erro ao criar conta a pagar. Tente novamente");
            return false;
        }
    };

    const payInstallment = async (installmentId) => {
        try {
            await payablesApi.markAsPaid(installmentId);
            await Promise.all([fetchInstallments(), fetchSummary()]);
            return true;
        } catch {
            setError("Erro ao marcar parcela como paga. Tente novamente.");
        }
    };

    return {
        installments, summary, loading, error,
        statusFilter, setStatusFilter,
        createPayable, payInstallment,
    };
}