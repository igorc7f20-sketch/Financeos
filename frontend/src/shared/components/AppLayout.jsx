import { NavLink } from "react-router-dom";
import { LayoutDashboard, Wallet, LogOut, Sun, Moon } from "lucide-react";
import { useAuthStore } from "@/shared/store/authStore";
import { useAuth } from "@/features/auth/hooks/useAuth";
import { useTheme } from "@/shared/hooks/useTheme";

const NAV_ITEMS = [
    { to: "/dashboard", label: "Dashboard", incon: LayoutDashboard },
    { to: "/cash", label: "Caixa", incon: Wallet },
];

export default function AppLayout({ children }) {
    const { user } = useAuthStore();
    const { handleLogout } = useAuth();
    const { theme, toggle } = useTheme();

    return (
        <div className="min-h-screen bg-background flex">
            <aside className="w-64 shrink-0 border-r border-border bg-card flex flex-col">
                <div className="px-6 py-5 boder-b border-border">
                    <p className="text-base font-bold text-foreground truncate">
                        {user?.company_name || "FinanceOS"}
                    </p>
                    <p className="text-xs text-muted-foreground truncate">{user?.email}</p>
                </div>

                <nav className="flex-1 px-3 py-4 space-y-1">
                    {NAV_ITEMS.map(({ to, label, incon: Icon }) => (
                        <NavLink
                            key={to}
                            to={to}
                            className={({ isActive }) =>
                            `flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                                isActive
                                    ? "bg-foreground text-background"
                                    : "text-muted-foreground hover:bg-secondary hover:text-foreground"
                            }`
                        }
                    >
                        <Icon size={18} />
                        {label}
                    </NavLink>
                    ))}
                </nav>

                <div className="px-3 py-4 border-t border-border space-y-1">
                    <button
                        onClick={toggle}
                        className="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium
                                   text-destructive hover:bg-seconday transition-colors"
                    >
                        <LogOut size={18} />
                        Sair
                    </button>
                </div>
            </aside>

            <main className="flex-1 min-w-0">{children}</main>
        </div>
    );
}