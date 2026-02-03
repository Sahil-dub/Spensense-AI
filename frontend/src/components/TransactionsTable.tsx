"use client";

import { useState } from "react";
import { httpDelete } from "@/lib/http";

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

export default function TransactionsTable({
  rows,
  onChanged,
}: {
  rows: Tx[];
  onChanged?: () => void;
}) {
  const [busyId, setBusyId] = useState<number | null>(null);
  const [msg, setMsg] = useState<string>("");

  async function remove(id: number) {
    setMsg("");
    setBusyId(id);
    try {
      await httpDelete(`/transactions/${id}`);
      setMsg("Deleted ✅");
      onChanged?.();
    } catch (e: any) {
      setMsg(`Delete failed: ${e?.message ?? "unknown"}`);
    } finally {
      setBusyId(null);
    }
  }

  return (
    <section className="border p-4 rounded space-y-3">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-semibold">Latest transactions</h2>
        {msg ? <p className="text-sm">{msg}</p> : null}
      </div>

      <div className="overflow-x-auto">
        <table className="min-w-full text-sm">
          <thead className="border-b">
            <tr className="text-left">
              <th className="py-2 pr-4">Date</th>
              <th className="py-2 pr-4">Type</th>
              <th className="py-2 pr-4">Category</th>
              <th className="py-2 pr-4">Bucket</th>
              <th className="py-2 pr-4">Amount</th>
              <th className="py-2 pr-4">Note</th>
              <th className="py-2 pr-2">Action</th>
            </tr>
          </thead>

          <tbody>
            {rows.length === 0 ? (
              <tr>
                <td className="py-3 text-gray-500" colSpan={7}>
                  No transactions yet.
                </td>
              </tr>
            ) : (
              rows.map((t) => (
                <tr key={t.id} className="border-b">
                  <td className="py-2 pr-4">{t.occurred_on}</td>
                  <td className="py-2 pr-4">{t.tx_type}</td>
                  <td className="py-2 pr-4">{t.category ?? "-"}</td>
                  <td className="py-2 pr-4">{t.bucket ?? "-"}</td>
                  <td className="py-2 pr-4">
                    {t.currency} {t.amount}
                  </td>
                  <td className="py-2 pr-4">{t.note ?? "-"}</td>
                  <td className="py-2 pr-2">
                    <button
                      onClick={() => remove(t.id)}
                      disabled={busyId === t.id}
                      className="px-3 py-1 rounded border disabled:opacity-60"
                    >
                      {busyId === t.id ? "..." : "Delete"}
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </section>
  );
}
