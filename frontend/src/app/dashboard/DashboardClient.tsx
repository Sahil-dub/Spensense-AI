"use client";

import { useCallback, useEffect, useMemo, useState} from "react";
import QuickAddTransaction from "@/components/QuickAddTransaction";
import TrasactionTable from "@/components/TransactionTable";
import MonthlyChart from "@/components/MonthlyChart";

const Base_URL = process.env.NEXT_PUBLIC_API_URL;

type AnalyticsSummary = {
    totals: {
        income:string;
        expense:string;
        net:string;
    };
    monthly: {
        month:string;
        income:string;
        expense:string;
        net:string;
    }[];
};

type Alert = {
    catergory: string;
    monthly_limit: string;
    spent: string;
    over_by: string;
};

type Transaction = {
    id: string;
    tx_type: "income" | "expense";
    amount: string;
    currency: string;
    category: string| null;
    bucket: string| null;
    occurred_on: string;
    notes: string| null;
};

async function apiGet<T>(path:string): Promise<T> {
    const res = await fetch(`${Base_URL}${path}`, {
    cache: "no-store",
  });
    if (!res.ok) {
        throw new Error(`GET ${path} failed: ${res.status}`);
    }
    return res.json();
}

export default function DashboardClient() {
    const [loading, setLoading] = useState(true);
    const [err, setErr] = useState<string>("");

    const [analytics, setAnalytics] = useState<AnalyticsSummary | null>(null);
    const [alerts, setAlerts] = useState<Alert[]>([]);
    const [Transactions, setTransactions] = useState<Transaction[]>([]);

    const reload = useCallback(async () => {
        setErr("");
        setLoading(true);
        try {
            const [a, al, txs] = await Promise.all([
                apiGet<AnalyticsSummary>("/analytics/summary?months=12&top_categories=10"),
                apiGet<{ alerts: Alert[] }>("/alerts"),
                apiGet<Transaction[]>("/transactions?limit=20&offset=0"),
            ]);
            setAnalytics(a);
            setAlerts(al.alerts);
            setTransactions(txs);
        }
        catch (e:any) {
            setErr(e?.message ?? "Failed to load dashboard");
        }
        finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        reload();
    }, [reload]);

    const totals = analytics?.totals;

    return (
        <main className="p-8 space-y-6" >
            <div className="flex items-end justify-between gap-4">
                <div>
                    <h1 className="text-3xl font-bold">SpendSense AI</h1>
                    <p className="text-sm text-gray-500">Dashboard</p>
                </div>
                <button
                    onClick={reload}
                    className="px-4 py-2 rounded border hover:bg-gray-50"
                    disabled={loading}
                    title="Refresh Data"
                >
                    Refresh
                </button>
            </div>

            {err ? (
                <div className="border rounded p-4 text-red-700">
                    <p className="font-semibold">Error</p>
                    <p className="text-sm">{err}</p>
                </div>
            ) : null}

        <section className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="p-4 rounded border">
                <p className="text-sm text-gray-500">Income</p>
                <p className="text-xl font-semibold">{totals ? `€${totals.income}` : "-"}</p>
            </div>
            <div className="p-4 rounded border">
                <p className="text-sm text-gray-500">Expenses</p>
                <p className="text-xl font-semibold">{totals ? `€${totals.expense}` : "-"}</p>
            </div>
            <div className="p-4 rounded border">
                <p className="text-sm text-gray-500">Net</p>
                <p className="text-xl font-semibold">{totals ? `€${totals.net}` : "-"}</p>
            </div>
        </section>

        <QuickAddTransaction onCreated={reload}/>

        <section className="border p-4 rounded space-y-2">
            <h2 className="text-xl font-semibold">Alerts</h2>
            {loading ? (
                <p className="text-sm text-gray-500">Loading...</p>
            ) : alerts.length === 0 ? (
                <p className="text-green-600">No Budget Alerts</p>
            ) : (
                <ul className="list-disc pl-6">
                    {alerts.map((a) => (
                        <li key={a.category}>
                            <span className="font-medium">{a.category}</span> over by €{a.over_by}
                        </li>
                    ))}
                </ul>
            )}
        </section>

        <MonthlyChart monthly = {analytics?.monthly ?? []} />

        <TrasactionTable items={Transactions} onDeleted={reload} />
    </main>
    );
}