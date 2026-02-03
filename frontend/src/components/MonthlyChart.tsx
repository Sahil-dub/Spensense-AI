"use client";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
} from "recharts";

type Row = {
  month: string; // YYYY-MM
  income: string;
  expense: string;
  net: string;
};

export default function MonthlyChart({ data }: { data: Row[] }) {
  // Convert string numbers -> Number for charts
  const rows = data.map((r) => ({
    month: r.month,
    income: Number(r.income),
    expense: Number(r.expense),
    net: Number(r.net),
  }));

  return (
    <section className="border p-4 rounded space-y-3">
      <h2 className="text-xl font-semibold">Monthly trend</h2>
      <div className="h-72">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={rows}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="month" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="income" />
            <Line type="monotone" dataKey="expense" />
            <Line type="monotone" dataKey="net" />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </section>
  );
}
