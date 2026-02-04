"use client";

import { useTheme } from "next-themes";
import { use, useEffect, useState } from "react";

export default function ThemeToggle() {
    const { theme, setTheme } = useTheme();
    const [mounted, setMounted] = useState(false);

    useEffect(() => setMounted(true), []);
    if(!mounted) return null;

    const isDark = theme === "dark";

    return(
        <button
            className="px-3 py-2 rounded border text-sm bg-white text-black border-zinc-300 dark:bg-zinc-900 dark:text-white dark:border-zinc-700"
            onClick={() => setTheme(isDark ? "light" : "dark")}
            type="button"
            title="Toggle Theme"
        >
            {isDark ? "🌙 Dark" : "☀️ Light"}
            </button>
    );
}