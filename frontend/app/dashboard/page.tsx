import { redirect } from "next/navigation";
import { getCurrentUser } from "@/lib/auth/http/helpers";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { SignOutButton } from "./SignOutButton";

/**
 * Protected Dashboard Page
 * 
 * Example of a protected route that requires authentication.
 * Uses getCurrentUser() helper to check authentication.
 * 
 * Route: /dashboard
 */
export default async function DashboardPage() {
  const user = await getCurrentUser();

  // Redirect to login if not authenticated
  // (Middleware also handles this, but this is a backup)
  if (!user) {
    redirect("/login");
  }

  // Redirect to tasks page (main application)
  redirect("/tasks");

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background to-primary/5 p-8">
      <div className="max-w-4xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-primary via-accent to-primary bg-clip-text text-transparent">
            Dashboard
          </h1>
          <p className="text-muted-foreground">
            Welcome to your protected dashboard
          </p>
        </div>

        <Card className="border-accent/20 shadow-lg shadow-accent/5">
          <CardHeader>
            <CardTitle>User Information</CardTitle>
            <CardDescription>Your authenticated session details</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <p className="text-sm text-muted-foreground">Email</p>
              <p className="text-lg font-medium">{user.email}</p>
            </div>
            {user.name && (
              <div>
                <p className="text-sm text-muted-foreground">Name</p>
                <p className="text-lg font-medium">{user.name}</p>
              </div>
            )}
            {user.image && (
              <div>
                <p className="text-sm text-muted-foreground">Profile Image</p>
                <img
                  src={user.image}
                  alt={user.name || user.email}
                  className="w-16 h-16 rounded-full mt-2"
                />
              </div>
            )}
            <div className="pt-4 border-t border-border">
              <SignOutButton />
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

