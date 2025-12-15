---
name: vercel-deployment
description: Vercel deployment for Next.js applications. Use when deploying frontend to Vercel, configuring environment variables, or troubleshooting deployment issues.
---

# Vercel Deployment

## Quick Deploy

```bash
npx vercel --prod
```

## Environment Variables

Set in Vercel Dashboard → Project → Settings → Environment Variables:
- `DATABASE_URL`
- `BETTER_AUTH_SECRET`
- `BETTER_AUTH_URL` (production URL)
- `NEXT_PUBLIC_API_URL`
- `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`

## Build Settings

- Framework: Next.js
- Build Command: `npm run build`
- Output Directory: `.next`
- Install Command: `npm ci`

## Common Issues

| Issue | Solution |
|-------|----------|
| Build fails | Check `npm run build` locally first |
| Environment variables not found | Redeploy after adding variables |
| Auth redirect issues | Update `BETTER_AUTH_URL` to Vercel URL |
| API routes 404 | Check `app/api/` structure |

## Deployment Checklist

- [ ] All env vars set in Vercel
- [ ] `npm run build` passes locally
- [ ] CORS configured for backend URL
- [ ] OAuth redirect URIs updated
