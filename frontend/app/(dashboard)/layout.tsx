import { ReactNode } from "react";
import { UserProfile } from "@/components/user/UserProfile";

export default function DashboardLayout({
  children,
}: {
  children: ReactNode;
}) {
  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-white border-b border-gray-300 shadow-sm">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <h1 className="text-xl font-bold text-gray-900">Todo App</h1>
          <UserProfile />
        </div>
      </nav>
      <main className="container mx-auto px-4 py-8">{children}</main>
    </div>
  );
}
