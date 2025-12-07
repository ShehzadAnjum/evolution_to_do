# Fixing Google OAuth "Invalid Origin" Error

## Problem
When trying to login through Google, you get an "Invalid Origin" error. This can happen for two reasons:

1. **Port Mismatch**: Your Next.js app is running on a different port (e.g., 3001) than what Better-Auth is configured for (e.g., 3000)
2. **Missing Redirect URI**: The redirect URI in Google Cloud Console doesn't match what Better-Auth is sending

**Note**: The code has been updated to automatically handle dynamic ports in development mode. However, you still need to configure Google Cloud Console correctly.

## Solution

### Step 1: Determine Your App URL

**For Local Development:**
- Your `BETTER_AUTH_URL` should be: `http://localhost:3000` (or whatever port your Next.js app runs on)
- Check your `.env.local` file in the `frontend` directory

**For Production (Vercel):**
- Your `BETTER_AUTH_URL` should be: `https://your-app.vercel.app` (your actual Vercel URL)
- This should match your deployed frontend URL

### Step 2: Configure Google Cloud Console

1. **Go to Google Cloud Console**
   - Visit: https://console.cloud.google.com
   - Select your project (or create one if you haven't)

2. **Navigate to OAuth Credentials**
   - Go to: **APIs & Services** → **Credentials**
   - Find your OAuth 2.0 Client ID (the one with `GOOGLE_CLIENT_ID`)
   - Click to edit it

3. **Add Authorized Redirect URIs**
   
   Based on your `BETTER_AUTH_URL`, add these redirect URIs:

   **For Local Development:**
   Add redirect URIs for common ports (Next.js might use different ports if 3000 is busy):
   ```
   http://localhost:3000/api/auth/callback/google
   http://localhost:3001/api/auth/callback/google
   http://localhost:3002/api/auth/callback/google
   ```
   
   Or add just the port you're currently using. Check your terminal - it will show:
   ```
   ▲ Next.js 14.2.33
   - Local:        http://localhost:3001
   ```
   
   **For Production:**
   ```
   https://your-app.vercel.app/api/auth/callback/google
   ```
   
   **For Both (Recommended):**
   Add BOTH local and production redirect URIs:
   ```
   http://localhost:3000/api/auth/callback/google
   http://localhost:3001/api/auth/callback/google
   https://your-app.vercel.app/api/auth/callback/google
   ```

   **Important Notes:**
   - ✅ Include the protocol (`http://` or `https://`)
   - ✅ Include the full path: `/api/auth/callback/google`
   - ✅ No trailing slash
   - ✅ Match the exact URL from your `BETTER_AUTH_URL` environment variable

4. **Save Changes**
   - Click **Save**
   - Wait a few minutes for changes to propagate (can take 1-5 minutes)

### Step 3: Verify Environment Variables

Check your environment variables are set correctly:

**Local Development (`.env.local` in `frontend/` directory):**
```env
BETTER_AUTH_URL=http://localhost:3000
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
```

**Production (Vercel Environment Variables):**
```env
BETTER_AUTH_URL=https://your-app.vercel.app
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
```

### Step 4: Restart Your Development Server

After making changes:

```bash
# Stop your Next.js dev server (Ctrl+C)
# Then restart it
cd frontend
npm run dev
```

### Step 5: Test Again

1. Clear your browser cookies for the site
2. Try logging in with Google again
3. The "Invalid Origin" error should be resolved

## Common Issues

### Issue: Still getting "Invalid Origin" after adding redirect URI

**Solutions:**
1. **Wait longer**: Google can take 1-5 minutes to propagate changes
2. **Double-check the URL**: 
   - Must match `BETTER_AUTH_URL` exactly
   - Must include `/api/auth/callback/google` path
   - Check for typos (http vs https, port numbers, domain)
3. **Check for trailing slashes**: Should NOT have trailing slash
4. **Verify environment variable**: Restart dev server after changing `.env.local`
5. **Clear browser cache**: Hard refresh (Ctrl+Shift+R or Cmd+Shift+R)

### Issue: Redirect URI doesn't match in production vs development

**Solution:** Add BOTH redirect URIs in Google Cloud Console:
- One for local: `http://localhost:3000/api/auth/callback/google`
- One for production: `https://your-app.vercel.app/api/auth/callback/google`

### Issue: Can't find the OAuth Client ID in Google Cloud Console

**Solution:**
1. Make sure you're in the correct Google Cloud project
2. Go to **APIs & Services** → **Credentials**
3. Look for **OAuth 2.0 Client IDs**
4. If you don't have one, create one:
   - Click **Create Credentials** → **OAuth client ID**
   - Application type: **Web application**
   - Name: Your app name
   - Add the redirect URIs as described above

## Quick Checklist

- [ ] Found my `BETTER_AUTH_URL` environment variable value
- [ ] Opened Google Cloud Console → APIs & Services → Credentials
- [ ] Found/created OAuth 2.0 Client ID
- [ ] Added redirect URI: `{BETTER_AUTH_URL}/api/auth/callback/google`
- [ ] Saved changes in Google Cloud Console
- [ ] Waited 1-5 minutes for propagation
- [ ] Verified `.env.local` has correct `BETTER_AUTH_URL`
- [ ] Restarted Next.js dev server
- [ ] Cleared browser cache/cookies
- [ ] Tested Google login again

## Still Having Issues?

If you're still experiencing problems:

1. **Check browser console** for detailed error messages
2. **Check server logs** for any Better-Auth errors
3. **Verify the callback URL** by checking what Better-Auth is actually sending:
   - Look at the network tab in browser dev tools
   - Find the Google OAuth request
   - Check the `redirect_uri` parameter
   - Ensure it matches exactly what you added in Google Cloud Console

The redirect URI format should be:
```
{BETTER_AUTH_URL}/api/auth/callback/google
```

Example:
- If `BETTER_AUTH_URL=http://localhost:3000`, then redirect URI = `http://localhost:3000/api/auth/callback/google`
- If `BETTER_AUTH_URL=https://myapp.vercel.app`, then redirect URI = `https://myapp.vercel.app/api/auth/callback/google`


