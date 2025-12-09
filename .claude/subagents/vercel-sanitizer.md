# Vercel Sanitizer Subagent

**Type**: Validator
**Used For**: Scanning for Vercel incompatibilities before deployment
**Version**: 1.0.0

## Purpose

Scan frontend code for patterns that break on Vercel serverless runtime.

## Check List

### ❌ Node-Only APIs in Server Components
```typescript
// BAD
import fs from 'fs'
export default function Page() {
  const data = fs.readFileSync('file.txt')  // Breaks on Vercel
}
```

### ❌ Direct process.env Access
```typescript
// BAD
const url = process.env.API_URL  // May be undefined

// GOOD
import { env } from '@/lib/config/env'
const url = env.API_URL  // Validated
```

### ❌ Missing NEXT_PUBLIC_ Prefix
```typescript
// BAD - used in client component
const url = process.env.API_URL

// GOOD
const url = process.env.NEXT_PUBLIC_API_URL
```

## Scan Process

1. Grep for `import fs` in app/ directory
2. Grep for `import path` in app/ directory
3. Grep for `process.env` without NEXT_PUBLIC in client components
4. Check next.config.js compatibility
5. Verify all env vars in Vercel dashboard

## Report Format

```
⚠️ Vercel Compatibility Issues Found:

1. app/page.tsx:15 - Using fs.readFileSync in Server Component
   Fix: Move to API route or use external data source

2. components/TaskList.tsx:23 - process.env.API_URL in client component
   Fix: Use NEXT_PUBLIC_API_URL instead

Total Issues: 2 critical, 0 warnings
```

---

**Related**: Vercel Deployment Agent, Frontend Web Agent
