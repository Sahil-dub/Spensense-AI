"use client";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
  Legend,
} from "recharts";

type Row = {
  month: string; // YYYY-MM
  income: string;
  expense: string;
  net: string;
};

export default function MonthlyChart({ data }: { data: Row[] }) {
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
          <LineChart data={rows} margin={{ top: 10, right: 20, left: 0, bottom: 30 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis
              dataKey="month"
              interval="preserveStartEnd"
              tickMargin={8}
              angle={-35}
              textAnchor="end"
            />
            <YAxis />
            <Tooltip />
            <Legend />

            <Line type="monotone" dataKey="income" stroke="#16a34a" strokeWidth={2} dot={false} />
            <Line type="monotone" dataKey="expense" stroke="#dc2626" strokeWidth={2} dot={false} />
            <Line type="monotone" dataKey="net" stroke="#2563eb" strokeWidth={2} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </section>
  );
}
