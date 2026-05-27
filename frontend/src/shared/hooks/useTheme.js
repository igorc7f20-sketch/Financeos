/**
 * useTheme - Shared Hook
 * 
 * Manages darj/ligth mode toggle.
 * Persists preference in localStorage
 * Aplies "dark" class to <html> element.
 */
import { useEffect, useState } from "react";

export function useTheme() {
    const [theme, setTheme] = useState
        (() => localStorage.getItem("theme") || "light"
    );

    useEffect(() => {
        const root = window.document.documentElement;
        root.classList.remove("light", "dark");
        root.classList.add(theme);
        localStorage.setItem("theme", theme);
    }, [theme]);

    const toggle = () => setTheme((t) => (t === "light" ? "dark" : "light"));

    return { theme, toggle };
}
        