"use client";

import { useEffect, useMemo, useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
  Brush,
} from "recharts";
import { httpGet } from "@/lib/http";

type Point = {
  date: string; // YYYY-MM-DD
  income: string;
  expense: string;
  net: string;
};

function eur(n: number) {
  if (!Number.isFinite(n)) return "€0";
  return new Intl.NumberFormat("de-DE", { style: "currency", currency: "EUR" }).format(n);
}

function formatDateLabel(iso: string) {
  // "YYYY-MM-DD" -> "DD.MM"
  const [y, m, d] = iso.split("-");
  return `${d}.${m}`;
}

function CustomTooltip({ active, payload, label, showSavings }: any) {
  if (!active || !payload?.length) return null;

  const v = Number(payload[0]?.value ?? 0);
  return (
    <div className="rounded border p-3 text-sm bg-white text-black border-zinc-300 dark:bg-zinc-900 dark:text-white dark:border-zinc-700">
      <div className="font-semibold mb-1">{label}</div>
      <div>{showSavings ? `Savings: ${eur(v)}` : `Expense: ${eur(v)}`}</div>
    </div>
  );
}

export default function DailyTrendChart() {
  const [fromDate, setFromDate] = useState<string>(() => {
    const d = new Date();
    d.setDate(d.getDate() - 30);
    return d.toISOString().slice(0, 10);
  });
  const [toDate, setToDate] = useState<string>(() => new Date().toISOString().slice(0, 10));

  const [showSavings, setShowSavings] = useState(false);

  const [points, setPoints] = useState<Point[]>([]);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState("");

  useEffect(() => {
    async function load() {
      setErr("");
      setLoading(true);
      try {
        const res = await httpGet<{ points: Point[] }>(
          `/analytics/daily?date_from=${fromDate}&date_to=${toDate}`
        );
        setPoints(res.points);
      } catch (e: any) {
        setErr(e?.message ?? "Failed to load daily analytics");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [fromDate, toDate]);

  const rows = useMemo(() => {
    return points.map((p) => ({
      date: p.date,
      expense: Number(p.expense),
      savings: Number(p.net), // net = savings in this view
    }));
  }, [points]);

  return (
    <section className="border p-4 rounded space-y-4">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-3">
        <h2 className="text-xl font-semibold">Daily trend</h2>

        <label className="flex items-center gap-2 text-sm cursor-pointer">
          <input
            type="checkbox"
            checked={showSavings}
            onChange={(e) => setShowSavings(e.target.checked)}
          />
          Show savings (net)
        </label>
      </div>

      <div className="flex flex-col md:flex-row md:items-end gap-3 text-sm">
        <div className="flex flex-col">
          <span className="text-gray-500 dark:text-zinc-300 mb-1">From date</span>
          <input
            type="date"
            value={fromDate}
            onChange={(e) => setFromDate(e.target.value)}
            className="border rounded p-2 bg-white text-black border-zinc-300 dark:bg-zinc-900 dark:text-white dark:border-zinc-700"
          />
        </div>
        <div className="flex flex-col">
          <span className="text-gray-500 dark:text-zinc-300 mb-1">To date</span>
          <input
            type="date"
            value={toDate}
            onChange={(e) => setToDate(e.target.value)}
            className="border rounded p-2 bg-white text-black border-zinc-300 dark:bg-zinc-900 dark:text-white dark:border-zinc-700"
          />
        </div>
        <button
          className="px-3 py-2 rounded border h-[42px]"
          type="button"
          onClick={() => {
            const d = new Date();
            const to = d.toISOString().slice(0, 10);
            d.setDate(d.getDate() - 30);
            const from = d.toISOString().slice(0, 10);
            setFromDate(from);
            setToDate(to);
          }}
        >
          Last 30 days
        </button>
      </div>

      {loading ? <p>Loading…</p> : null}
      {err ? <p className="text-red-600">Error: {err}</p> : null}

      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={rows} margin={{ top: 10, right: 20, left: 0, bottom: 25 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis
              dataKey="date"
              tickFormatter={(v) => formatDateLabel(String(v))}
              interval="preserveStartEnd"
              angle={-30}
              textAnchor="end"
              tickMargin={10}
            />
            <YAxis />
            <Tooltip content={(p) => <CustomTooltip {...p} showSavings={showSavings} />} />

            {!showSavings ? (
              <Line
                type="monotone"
                dataKey="expense"
                stroke="#dc2626"
                strokeWidth={2}
                dot={false}
                activeDot={{ r: 5 }}
                isAnimationActive
                animationDuration={450}
              />
            ) : (
              <Line
                type="monotone"
                dataKey="savings"
                stroke="#2563eb"
                strokeWidth={2}
                dot={false}
                activeDot={{ r: 5 }}
                isAnimationActive
                animationDuration={450}
              />
            )}

            <Brush dataKey="date" height={30} travellerWidth={10} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </section>
  );
}
