import { ReactNode } from "react";
import { UserProfile } from "@/components/user/UserProfile";
import { ThemeToggle } from "@/components/ui/theme-toggle";
import { VERSION_DISPLAY } from "@/lib/version";

export default function DashboardLayout({
  children,
}: {
  children: ReactNode;
}) {
  return (
    <div className="h-screen w-screen overflow-hidden flex flex-col bg-slate-100 dark:bg-slate-950">
      {/* Sticky Header - NEVER scrolls */}
      <nav className="flex-none h-14 bg-white dark:bg-card border-b border-gray-300 dark:border-border shadow-sm z-50">
        <div className="h-full px-4 lg:px-6 flex items-center justify-between">
          <div className="flex items-baseline gap-2">
            <h1 className="text-xl font-bold text-gray-900 dark:text-foreground">Todo App</h1>
            <span className="text-[10px] text-yellow-500 dark:text-yellow-400 font-medium">{VERSION_DISPLAY}</span>
          </div>
          <div className="flex items-center gap-3">
            <ThemeToggle />
            <UserProfile />
          </div>
        </div>
      </nav>
      {/* Main content area - scrollable */}
      <main className="flex-1 overflow-hidden">{children}</main>
    </div>
  );
}
