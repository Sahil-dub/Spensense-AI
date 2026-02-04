"use client";

import { useCallback, useEffect, useState } from "react";
import QuickAddTransaction from "@/components/QuickAddTransaction";
import TransactionsTable from "@/components/TransactionsTable";
import MonthlyChart from "@/components/MonthlyChart";
import CategoryPie from "@/components/CategoryPie";
import { httpGet } from "@/lib/http";
import ThemeToggle from "./ThemeToggle";

type Analytics = {
  totals: { income: string; expense: string; net: string };
  monthly: { month: string; income: string; expense: string; net: string }[];
};

type Alerts = { alerts: { category: string; over_by: string }[] };

type Tx = {
  id: number;
  tx_type: "income" | "expense";
  amount: string; // from backend Decimal
  currency: string;
  category: string | null;
  bucket: string | null;
  occurred_on: string; // YYYY-MM-DD
  note: string | null;
};

type PieSlice = { name: string; value: number };

function groupByCategory(rows: Tx[], txType: "income" | "expense"): PieSlice[] {
  const map = new Map<string, number>();

  for (const r of rows) {
    if (r.tx_type !== txType) continue;
    const key = (r.category ?? "uncategorized").toString().trim() || "uncategorized";
    const val = Number(r.amount);
    if (!Number.isFinite(val) || val <= 0) continue;
    map.set(key, (map.get(key) ?? 0) + val);
  }

  return Array.from(map.entries()).map(([name, value]) => ({ name, value }));
}

export default function DashboardClient() {
  const [months, setMonths] = useState<number>(12);

  const [analytics, setAnalytics] = useState<Analytics | null>(null);
  const [alerts, setAlerts] = useState<Alerts | null>(null);
  const [txs, setTxs] = useState<Tx[]>([]);

  const [incomePie, setIncomePie] = useState<PieSlice[]>([]);
  const [expensePie, setExpensePie] = useState<PieSlice[]>([]);

  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState<string>("");

  const load = useCallback(async () => {
    setErr("");
    setLoading(true);

    try {
      const [a, al, t] = await Promise.all([
        httpGet<Analytics>(`/analytics/summary?months=${months}&top_categories=10`),
        httpGet<Alerts>("/alerts"),
        httpGet<Tx[]>("/transactions?limit=200&offset=0"), // increase for better pies
      ]);

      setAnalytics(a);
      setAlerts(al);
      setTxs(t);

      setIncomePie(groupByCategory(t, "income"));
      setExpensePie(groupByCategory(t, "expense"));
    } catch (e: any) {
      setErr(e?.message ?? "Failed to load data");
    } finally {
      setLoading(false);
    }
  }, [months]);

  useEffect(() => {
    load();
  }, [load]);

  if (loading) return <main className="p-8">Loading…</main>;
  if (err) return <main className="p-8 text-red-600">Error: {err}</main>;
  if (!analytics || !alerts) return <main className="p-8">No data</main>;

  return (
    <main className="p-8 space-y-6">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-3">
        <h1 className="text-3xl font-bold">SpendSense AI</h1>

        <div className="flex items-center gap-3">
          <ThemeToggle />
          <label className="text-sm text-gray-500">Range</label>
          <select
            className="border rounded p-2"
            value={months}
            onChange={(e) => setMonths(Number(e.target.value))}
          >
            <option value={3}>Last 3 months</option>
            <option value={6}>Last 6 months</option>
            <option value={12}>Last 12 months</option>
            <option value={24}>Last 24 months</option>
          </select>

          <button className="px-4 py-2 rounded border" onClick={load}>
            Refresh
          </button>
        </div>
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

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <CategoryPie title="Income by category" data={incomePie} />
        <CategoryPie title="Expense by category" data={expensePie} />
      </div>

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

      <TransactionsTable rows={txs.slice(0, 20)} onChanged={load} />
    </main>
  );
}
