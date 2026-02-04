export const INCOME_CATEGORIES = [
  "salary",
  "freelance",
  "scholarship",
  "investment",
  "dividend",
  "refund",
  "gift",
  "other",
] as const;

export const EXPENSE_CATEGORIES = [
    "rent",
    "utilities",
    "health insarance",
    "groceries",
    "transport",
    "dining out",
    "shopping",
    "entertainment",
    "phone bills",
    "education",
    "travel",
    "gym",
    "medical",
    "others",
] as const;

export type IncomeCategory = (typeof INCOME_CATEGORIES)[number];
export type ExpenseCategory = (typeof EXPENSE_CATEGORIES)[number];
