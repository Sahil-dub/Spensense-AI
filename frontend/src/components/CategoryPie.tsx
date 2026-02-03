"use client";

import { ResponsiveContainer, PieChart, Pie, Tooltip, Cell, Legend } from "recharts";

type Slice = { name: string; value: number };

const COLORS = [
  "#2563eb",
  "#16a34a",
  "#dc2626",
  "#f59e0b",
  "#7c3aed",
  "#0ea5e9",
  "#64748b",
  "#db2777",
];

export default function CategoryPie({ title, data }: { title: string; data: Slice[] }) {
  const cleaned = data
    .filter((d) => d.value > 0)
    .sort((a, b) => b.value - a.value)
    .slice(0, 8); // top 8 for readability

  return (
    <section className="border p-4 rounded space-y-3">
      <h2 className="text-xl font-semibold">{title}</h2>

      {cleaned.length === 0 ? (
        <p className="text-sm text-gray-500">No data</p>
      ) : (
        <div className="h-72">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie data={cleaned} dataKey="value" nameKey="name" outerRadius={95}>
                {cleaned.map((_, idx) => (
                  <Cell key={idx} fill={COLORS[idx % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
      )}
    </section>
  );
}
