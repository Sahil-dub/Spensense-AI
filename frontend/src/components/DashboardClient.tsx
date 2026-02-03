"use client";

import { useCallback, useEffect, useState } from "react";
import QuickAddTransaction from "@/components/QuickAddTransaction";
import TransactionsTable from "@/components/TransactionsTable";
import MonthlyChart from "@/components/MonthlyChart";
import { httpGet } from "@/lib/http";

type Analytics = {
  totals: { income: string; expense: string; net: string };
  monthly: { month: string; income: string; expense: string; net: string }[];
};

type Alerts = { alerts: { category: string; over_by: string }[] };

type Tx = {
  id: number;
  tx_type: "income" | "expense";
  amount: string;
  currency: string;
  category: string | null;
  bucket: string | null;
  occurred_on: string;
  note: string | null;
};

export default function DashboardClient() {
  const [analytics, setAnalytics] = useState<Analytics | null>(null);
  const [alerts, setAlerts] = useState<Alerts | null>(null);
  const [txs, setTxs] = useState<Tx[]>([]);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState<string>("");

  const load = useCallback(async () => {
    setErr("");
    setLoading(true);
    try {
      const [a, al, t] = await Promise.all([
        httpGet<Analytics>("/analytics/summary?months=12&top_categories=10"),
        httpGet<Alerts>("/alerts"),
        httpGet<Tx[]>("/transactions?limit=20&offset=0"),
      ]);
      setAnalytics(a);
      setAlerts(al);
      setTxs(t);
    } catch (e: any) {
      setErr(e?.message ?? "Failed to load data");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  if (loading) return <main className="p-8">Loading…</main>;
  if (err) return <main className="p-8 text-red-600">Error: {err}</main>;
  if (!analytics || !alerts) return <main className="p-8">No data</main>;

  return (
    <main className="p-8 space-y-6">
      <div className="flex items-center justify-between gap-4">
        <h1 className="text-3xl font-bold">SpendSense AI</h1>
        <button className="px-4 py-2 rounded border" onClick={load}>
          Refresh
        </button>
      </div>

      <section className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="p-4 rounded border">
          <p className="text-sm text-gray-500">Income</p>
          <p className="text-xl font-semibold">€{analytics.totals.income}</p>
        </div>
        <div className="p-4 rounded border">
          <p className="text-sm text-gray-500">Expense</p>
          <p className="text-xl font-semibold">€{analytics.totals.expense}</p>
        </div>
        <div className="p-4 rounded border">
          <p className="text-sm text-gray-500">Net</p>
          <p className="text-xl font-semibold">€{analytics.totals.net}</p>
        </div>
      </section>

      <QuickAddTransaction onCreated={load} />

      <MonthlyChart data={analytics.monthly} />

      <section className="border p-4 rounded">
        <h2 className="text-xl font-semibold mb-2">Alerts</h2>
        {alerts.alerts.length === 0 ? (
          <p className="text-green-600">No budget alerts 🎉</p>
        ) : (
          <ul className="list-disc pl-6">
            {alerts.alerts.map((a) => (
              <li key={a.category}>
                {a.category} over by €{a.over_by}
              </li>
            ))}
          </ul>
        )}
      </section>

      <TransactionsTable rows={txs} onChanged={load} />
    </main>
  );
}
