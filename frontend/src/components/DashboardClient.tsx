"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import QuickAddTransaction from "@/components/QuickAddTransaction";
import TransactionsTable from "@/components/TransactionsTable";
import CategoryPie from "@/components/CategoryPie";
import DailyTrendChart from "@/components/DailyTrendChart";
import ThemeToggle from "@/components/ThemeToggle";
import { httpGet } from "@/lib/http";

type Analytics = {
  totals: { income: string; expense: string; net: string };
  monthly: { month: string; income: string; expense: string; net: string }[];
};

type Alerts = { alerts: { category: string; over_by: string }[] };

type Tx = {
  id: number;
  tx_type: "income" | "expense";
  amount: string; // Decimal as string
  currency: string;
  category: string | null;
  bucket: string | null;
  occurred_on: string; // YYYY-MM-DD
  note: string | null;
};

type PieSlice = { name: string; value: number };

function inRange(iso: string, from: string, to: string) {
  // safe lexicographic compare for YYYY-MM-DD
  return iso >= from && iso <= to;
}

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
  // Shared date range for DAILY chart + pies
  const [fromDate, setFromDate] = useState(() => {
    const d = new Date();
    d.setDate(d.getDate() - 30);
    return d.toISOString().slice(0, 10);
  });
  const [toDate, setToDate] = useState(() => new Date().toISOString().slice(0, 10));

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
        httpGet<Tx[]>("/transactions?limit=500&offset=0"),
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

  // Pie charts filtered by the selected date range
  const filteredTxs = useMemo(() => {
    return txs.filter((x) => inRange(x.occurred_on, fromDate, toDate));
  }, [txs, fromDate, toDate]);

  const incomePie = useMemo(() => groupByCategory(filteredTxs, "income"), [filteredTxs]);
  const expensePie = useMemo(() => groupByCategory(filteredTxs, "expense"), [filteredTxs]);

  if (loading) return <main className="p-8">Loading…</main>;
  if (err) return <main className="p-8 text-red-600">Error: {err}</main>;
  if (!analytics || !alerts) return <main className="p-8">No data</main>;

  return (
    <main className="p-8 space-y-6">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-3">
        <h1 className="text-3xl font-bold">SpendSense AI</h1>

        <div className="flex items-center gap-3">
          <ThemeToggle />
          <button className="px-4 py-2 rounded border" onClick={load}>
            Refresh
          </button>
        </div>
      </div>

      <section className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="p-4 rounded border">
          <p className="text-sm text-gray-500 dark:text-zinc-300">Income</p>
          <p className="text-xl font-semibold">€{analytics.totals.income}</p>
        </div>
        <div className="p-4 rounded border">
          <p className="text-sm text-gray-500 dark:text-zinc-300">Expense</p>
          <p className="text-xl font-semibold">€{analytics.totals.expense}</p>
        </div>
        <div className="p-4 rounded border">
          <p className="text-sm text-gray-500 dark:text-zinc-300">Net</p>
          <p className="text-xl font-semibold">€{analytics.totals.net}</p>
        </div>
      </section>

      <QuickAddTransaction onCreated={load} />

      {/* Daily chart controls the date range, and pies follow the same range */}
      <DailyTrendChart
        fromDate={fromDate}
        toDate={toDate}
        onChangeRange={({ fromDate: f, toDate: t }) => {
          setFromDate(f);
          setToDate(t);
        }}
      />

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <CategoryPie title={`Income by category (${fromDate} → ${toDate})`} data={incomePie} />
        <CategoryPie title={`Expense by category (${fromDate} → ${toDate})`} data={expensePie} />
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

      {/* Table: show latest 20 from fetched list */}
      <TransactionsTable rows={txs.slice(0, 20)} onChanged={load} />
    </main>
  );
}
