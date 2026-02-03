"use client";

import { useState } from "react";

const BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

type TxType = "income" | "expense";
type Bucket = "necessary" | "controllable" | "unnecessary";

export default function QuickAddTransaction({ onCreated }: { onCreated?: () => void }) {
  const [txType, setTxType] = useState<TxType>("expense");
  const [amount, setAmount] = useState<string>("");
  const [category, setCategory] = useState<string>("dining_out");
  const [bucket, setBucket] = useState<Bucket>("controllable");
  const [occurredOn, setOccurredOn] = useState<string>(new Date().toISOString().slice(0, 10));
  const [note, setNote] = useState<string>("");

  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState<string>("");

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setMsg("");

    const amt = Number(amount);
    if (!amount || Number.isNaN(amt) || amt <= 0) {
      setMsg("Enter a valid amount > 0");
      return;
    }

    setLoading(true);
    try {
      const res = await fetch(`${BASE_URL}/transactions`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          tx_type: txType,
          amount: amt,
          currency: "EUR",
          category,
          bucket: txType === "expense" ? bucket : null,
          occurred_on: occurredOn,
          note: note || null,
        }),
      });

      if (!res.ok) {
        const text = await res.text();
        throw new Error(text || `HTTP ${res.status}`);
      }

      setAmount("");
      setNote("");
      setMsg("Saved ✅");
      onCreated?.();
    } catch (err: any) {
      setMsg(`Error: ${err?.message ?? "unknown"}`);
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="border p-4 rounded space-y-3">
      <h2 className="text-xl font-semibold">Quick Add Transaction</h2>

      <form onSubmit={submit} className="grid grid-cols-1 md:grid-cols-6 gap-3 items-end">
        <div className="md:col-span-1">
          <label className="text-sm text-gray-500">Type</label>
          <select
            className="w-full border rounded p-2"
            value={txType}
            onChange={(e) => setTxType(e.target.value as TxType)}
          >
            <option value="expense">expense</option>
            <option value="income">income</option>
          </select>
        </div>

        <div className="md:col-span-1">
          <label className="text-sm text-gray-500">Amount (€)</label>
          <input
            className="w-full border rounded p-2"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            placeholder="12.50"
            inputMode="decimal"
          />
        </div>

        <div className="md:col-span-1">
          <label className="text-sm text-gray-500">Category</label>
          <input
            className="w-full border rounded p-2"
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            placeholder="rent / dining_out"
          />
        </div>

        <div className="md:col-span-1">
          <label className="text-sm text-gray-500">Bucket</label>
          <select
            className="w-full border rounded p-2"
            value={bucket}
            onChange={(e) => setBucket(e.target.value as Bucket)}
            disabled={txType === "income"}
            title={txType === "income" ? "Bucket applies to expenses" : ""}
          >
            <option value="necessary">necessary</option>
            <option value="controllable">controllable</option>
            <option value="unnecessary">unnecessary</option>
          </select>
        </div>

        <div className="md:col-span-1">
          <label className="text-sm text-gray-500">Date</label>
          <input
            className="w-full border rounded p-2"
            type="date"
            value={occurredOn}
            onChange={(e) => setOccurredOn(e.target.value)}
          />
        </div>

        <div className="md:col-span-1">
          <label className="text-sm text-gray-500">Note</label>
          <input
            className="w-full border rounded p-2"
            value={note}
            onChange={(e) => setNote(e.target.value)}
            placeholder="optional"
          />
        </div>

        <div className="md:col-span-6 flex items-center gap-3">
          <button
            type="submit"
            disabled={loading}
            className="px-4 py-2 rounded bg-black text-white disabled:opacity-60"
          >
            {loading ? "Saving..." : "Save"}
          </button>
          {msg ? <p className="text-sm">{msg}</p> : null}
        </div>
      </form>
    </section>
  );
}
