"use client";

import { useMemo, useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
  Legend,
  Brush,
} from "recharts";

type Row = {
  month: string; // YYYY-MM
  income: string;
  expense: string;
  net: string;
};

function eur(n: number) {
  if (!Number.isFinite(n)) return "€0";
  return new Intl.NumberFormat("de-DE", { style: "currency", currency: "EUR" }).format(n);
}

function CustomTooltip({ active, payload, label }: any) {
  if (!active || !payload?.length) return null;

  const map = new Map<string, number>();
  for (const p of payload) {
    map.set(p.dataKey, Number(p.value));
  }

  return (
    <div className="rounded border p-3 text-sm bg-white text-black border-zinc-300
                    dark:bg-zinc-900 dark:text-white dark:border-zinc-700">
      <div className="font-semibold mb-1">{label}</div>
      <div className="flex flex-col gap-1">
        <div>Income: {eur(map.get("income") ?? 0)}</div>
        <div>Expense: {eur(map.get("expense") ?? 0)}</div>
        <div>Net: {eur(map.get("net") ?? 0)}</div>
      </div>
    </div>
  );
}

export default function MonthlyChart({ data }: { data: Row[] }) {
  const rows = useMemo(
    () =>
      data.map((r) => ({
        month: r.month,
        income: Number(r.income),
        expense: Number(r.expense),
        net: Number(r.net),
      })),
    [data]
  );

  const [selectedMonth, setSelectedMonth] = useState<string | null>(null);
  const selected = rows.find((r) => r.month === selectedMonth) ?? null;

  // Optional line toggles
  const [showIncome, setShowIncome] = useState(true);
  const [showExpense, setShowExpense] = useState(true);
  const [showNet, setShowNet] = useState(true);

  return (
    <section className="border p-4 rounded space-y-4">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-3">
        <h2 className="text-xl font-semibold">Monthly trend</h2>

        <div className="flex flex-wrap gap-3 text-sm">
          <label className="flex items-center gap-2 cursor-pointer">
            <input type="checkbox" checked={showIncome} onChange={(e) => setShowIncome(e.target.checked)} />
            Income
          </label>
          <label className="flex items-center gap-2 cursor-pointer">
            <input type="checkbox" checked={showExpense} onChange={(e) => setShowExpense(e.target.checked)} />
            Expense
          </label>
          <label className="flex items-center gap-2 cursor-pointer">
            <input type="checkbox" checked={showNet} onChange={(e) => setShowNet(e.target.checked)} />
            Net
          </label>
        </div>
      </div>

      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart
            data={rows}
            margin={{ top: 10, right: 20, left: 0, bottom: 40 }}
            onClick={(state: any) => {
              const label = state?.activeLabel;
              if (label) setSelectedMonth(label);
            }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis
              dataKey="month"
              interval="preserveStartEnd"
              tickMargin={10}
              angle={-35}
              textAnchor="end"
            />
            <YAxis tickFormatter={(v) => `${v}`} />
            <Tooltip content={<CustomTooltip />} />
            <Legend />

            {showIncome && <Line type="monotone" dataKey="income" stroke="#16a34a" strokeWidth={2} dot={false} />}
            {showExpense && <Line type="monotone" dataKey="expense" stroke="#dc2626" strokeWidth={2} dot={false} />}
            {showNet && <Line type="monotone" dataKey="net" stroke="#2563eb" strokeWidth={2} dot={false} />}

            {/* Drag to zoom */}
            <Brush dataKey="month" height={30} travellerWidth={10} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Selected month summary */}
      <div className="rounded border p-3 text-sm bg-white text-black border-zinc-300
                      dark:bg-zinc-900 dark:text-white dark:border-zinc-700">
        <div className="flex items-center justify-between gap-3">
          <div className="font-semibold">
            {selected ? `Selected: ${selected.month}` : "Click a month to inspect"}
          </div>
          {selected ? (
            <button
              className="px-3 py-1 rounded border"
              onClick={() => setSelectedMonth(null)}
              type="button"
            >
              Clear
            </button>
          ) : null}
        </div>

        {selected ? (
          <div className="mt-2 grid grid-cols-1 md:grid-cols-3 gap-3">
            <div className="p-3 rounded border">
              <div className="text-gray-500 dark:text-zinc-300">Income</div>
              <div className="font-semibold">{eur(selected.income)}</div>
            </div>
            <div className="p-3 rounded border">
              <div className="text-gray-500 dark:text-zinc-300">Expense</div>
              <div className="font-semibold">{eur(selected.expense)}</div>
            </div>
            <div className="p-3 rounded border">
              <div className="text-gray-500 dark:text-zinc-300">Net</div>
              <div className="font-semibold">{eur(selected.net)}</div>
            </div>
          </div>
        ) : null}
      </div>
    </section>
  );
}
