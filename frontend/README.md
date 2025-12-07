# Phase II Web Application - Frontend

Next.js 16+ frontend for the Evolution of Todo web application with Better Auth authentication and modern React components.

## Prerequisites

- Node.js 20+
- npm or yarn
- Neon PostgreSQL database (shared with backend)
- Backend API running (see backend README)

## Quick Start

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create .env.local file (see Environment Variables section)
cp .env.example .env.local
# Edit .env.local with your values

# Run Better Auth migrations (creates user tables in database)
npx @better-auth/cli migrate

# Start development server
npm run dev
```

**Verify**: Open http://localhost:3000

## Environment Variables

Create a `.env.local` file in the `frontend/` directory:

```bash
# Database (Neon PostgreSQL - same as backend)
DATABASE_URL=postgresql://user:password@host/database?sslmode=require

# Better Auth Configuration
# Must match BETTER_AUTH_SECRET in backend/.env
BETTER_AUTH_SECRET=your-32-character-secret-key-here-minimum-length

# Better Auth Base URL
BETTER_AUTH_URL=http://localhost:3000

# Next.js Public App URL
NEXT_PUBLIC_APP_URL=http://localhost:3000

# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Google OAuth (Optional - only if using Google sign-in)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

## Database Setup

### Run Better Auth Migrations

Better Auth needs to create the user tables in your database:

```bash
# From frontend directory
npx @better-auth/cli migrate
```

This creates:
- `user` table
- `session` table
- `account` table (for OAuth)
- Other Better Auth tables

**Important**: Run this before starting the backend, as the backend's `tasks` table has a foreign key to `user`.

## Development

### Run Development Server

```bash
npm run dev
```

The app will be available at http://localhost:3000

### Run Tests

```bash
# Run all tests
npm run test

# Run tests in watch mode
npm run test:watch
```

### Build for Production

```bash
npm run build
npm start
```

## Project Structure

```
frontend/
├── app/                      # Next.js App Router
│   ├── layout.tsx            # Root layout
│   ├── page.tsx             # Home page
│   ├── globals.css           # Global styles
│   │
│   ├── (auth)/               # Auth pages (no nav)
│   │   └── login/           # Login/signup page
│   │
│   ├── (dashboard)/         # Protected pages
│   │   ├── layout.tsx       # Dashboard layout with nav
│   │   └── tasks/          # Tasks page
│   │
│   └── api/                 # API routes
│       └── auth/            # Better Auth endpoints
│
├── components/
│   ├── ui/                  # Base UI components (shadcn/ui)
│   ├── tasks/               # Task components
│   │   ├── task-form.tsx
│   │   ├── task-list.tsx
│   │   ├── task-item.tsx
│   │   └── task-summary.tsx
│   └── auth/                # Auth components
│
├── lib/
│   ├── api.ts               # API client for backend
│   ├── auth-token.ts        # JWT token extraction
│   ├── types.ts             # TypeScript types
│   └── auth/                # Better Auth configuration
│       ├── core/
│       │   ├── server.ts    # Better Auth server
│       │   └── client.ts    # Better Auth client
│       └── adapters/
│           └── db-adapter.ts  # Database connection
│
├── public/                  # Static assets
├── package.json
├── tsconfig.json
├── next.config.js
└── tailwind.config.ts
```

## Features

- ✅ Next.js 16+ with App Router
- ✅ Better Auth authentication (email/password + Google OAuth)
- ✅ JWT token management
- ✅ Protected routes
- ✅ Task CRUD operations
- ✅ Responsive design with Tailwind CSS
- ✅ TypeScript for type safety
- ✅ Modern React components

## Technology Stack

- **Framework**: Next.js 16+ (App Router)
- **React**: 18.3+
- **Authentication**: Better Auth
- **Database**: Neon PostgreSQL (via Better Auth)
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui (Radix UI)
- **Type Safety**: TypeScript 5+

## Routes

### Public Routes
- `/` - Home page (redirects to login)
- `/login` - Login/signup page

### Protected Routes (Require Authentication)
- `/tasks` - Task management page
- `/dashboard` - Dashboard (redirects to /tasks)

## Authentication Flow

1. User signs up/logs in via Better Auth
2. Better Auth creates session in database
3. Frontend calls `/api/auth/token` to get JWT
4. JWT is sent to backend API in `Authorization: Bearer <token>` header
5. Backend validates JWT and extracts user ID
6. Backend filters tasks by user ID

## API Integration

The frontend communicates with the backend API via:

- **Base URL**: `NEXT_PUBLIC_API_URL` (default: http://localhost:8000)
- **Authentication**: JWT token from Better Auth session
- **Client**: `lib/api.ts` provides typed functions for all endpoints

See `lib/api.ts` for available API functions.

## Troubleshooting

### "Cannot connect to server"
- Ensure backend is running on port 8000
- Check `NEXT_PUBLIC_API_URL` is correct
- Verify CORS is configured in backend

### "Authentication required"
- Check Better Auth is configured correctly
- Verify `BETTER_AUTH_SECRET` matches backend
- Clear browser cookies and re-login

### "Database migration failed"
- Ensure `DATABASE_URL` is correct
- Check database connection is working
- Verify you have permissions to create tables

### "Module not found"
- Run `npm install` to install dependencies
- Check Node.js version (requires 20+)

## Production Deployment

### Vercel (Recommended)

1. Connect GitHub repository to Vercel
2. Set root directory: `frontend`
3. Add environment variables:
   - `DATABASE_URL`
   - `BETTER_AUTH_SECRET`
   - `BETTER_AUTH_URL` (your Vercel URL)
   - `NEXT_PUBLIC_APP_URL` (your Vercel URL)
   - `NEXT_PUBLIC_API_URL` (your backend URL)
4. Deploy

Vercel will automatically:
- Run `npm run build`
- Deploy to edge network
- Handle environment variables

### Other Platforms

For other platforms (Netlify, Railway, etc.), ensure:
- Node.js 20+ is available
- Environment variables are set
- Build command: `npm run build`
- Start command: `npm start`

## License

Part of the Evolution of Todo project for Hackathon II.

