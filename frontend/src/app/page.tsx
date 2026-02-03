import { apiGet } from "@/lib/api";
import QuickAddTransaction from "@/components/QuickAddTransaction";

type AnalyticsSummary = {
  totals: {
    income: string;
    expense: string;
    net: string;
  };
};

type Alert = {
  category: string;
  over_by: string;
};

export default async function DashboardPage() {
  const analytics = await apiGet<AnalyticsSummary>("/analytics/summary");
  const alerts = await apiGet<{ alerts: Alert[] }>("/alerts");

  return (
    <main className="p-8 space-y-6">
      <h1 className="text-3xl font-bold">SpendSense AI</h1>

      <section className="grid grid-cols-3 gap-4">
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

      <QuickAddTransaction />
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
    </main>
  );
}
