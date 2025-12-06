import Link from "next/link";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-8 bg-gradient-to-br from-background via-background to-primary/5">
      <div className="max-w-4xl w-full space-y-8">
        <div className="text-center space-y-4">
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-primary via-accent to-primary bg-clip-text text-transparent">
            Better Auth Module
          </h1>
          <p className="text-xl text-muted-foreground">
            Reusable authentication system for Next.js applications
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          <div className="rounded-xl border bg-card text-card-foreground border-accent/20 shadow-lg shadow-accent/5 p-6">
            <h2 className="text-2xl font-bold mb-2">Get Started</h2>
            <p className="text-muted-foreground mb-4">
              Sign in or create an account to access protected features
            </p>
            <Link href="/login">
              <button className="w-full rounded-md bg-gradient-to-r from-primary to-primary/80 hover:from-primary/90 hover:to-primary/70 text-primary-foreground px-4 py-2 font-medium transition-colors">
                Go to Login
              </button>
            </Link>
          </div>

          <div className="rounded-xl border bg-card text-card-foreground border-accent/20 shadow-lg shadow-accent/5 p-6">
            <h2 className="text-2xl font-bold mb-2">Features</h2>
            <p className="text-muted-foreground mb-4">
              What this authentication module provides
            </p>
            <div className="space-y-2 text-sm">
              <div className="flex items-center gap-2">
                <span className="text-accent">✓</span>
                <span>Email/Password Authentication</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-accent">✓</span>
                <span>Google OAuth Integration</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-accent">✓</span>
                <span>JWT Session Management</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-accent">✓</span>
                <span>Route Protection</span>
              </div>
            </div>
          </div>
        </div>

        <div className="text-center text-sm text-muted-foreground">
          <p>Built with Better-Auth, Next.js, Neon Postgres, and Tailwind CSS</p>
        </div>
      </div>
    </main>
  );
}

