# Fixing Google OAuth "invalid_client" Error

## Problem
You're getting "Error 401: invalid_client" with the message "The OAuth client was not found." This means Google cannot find the OAuth client ID you're using.

## Solution Steps

### Step 1: Verify Environment Variables Are Set

Check if your `.env.local` file (in the `frontend/` directory) has the Google OAuth credentials:

```bash
cd frontend
cat .env.local
```

You should see:
```env
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
```

**If these are missing or empty, continue to Step 2.**

### Step 2: Create OAuth Credentials in Google Cloud Console

1. **Go to Google Cloud Console**
   - Visit: https://console.cloud.google.com
   - Sign in with your Google account

2. **Select or Create a Project**
   - If you don't have a project, click "Create Project"
   - Give it a name (e.g., "Evolution Todo")
   - Click "Create"

3. **Enable Google+ API** (if needed)
   - Go to: **APIs & Services** → **Library**
   - Search for "Google+ API" or "Google Identity"
   - Click on it and click "Enable"

4. **Create OAuth 2.0 Client ID**
   - Go to: **APIs & Services** → **Credentials**
   - Click **+ CREATE CREDENTIALS** → **OAuth client ID**
   
   - If prompted, configure the OAuth consent screen first:
     - **User Type**: External (or Internal if you have Google Workspace)
     - **App name**: Evolution Todo (or your app name)
     - **User support email**: Your email
     - **Developer contact**: Your email
     - Click **Save and Continue**
     - Scopes: Just click **Save and Continue** (default is fine)
     - Test users: Add your email if needed, then **Save and Continue**

   - Back to creating OAuth client ID:
     - **Application type**: Web application
     - **Name**: Evolution Todo Web Client
     
     - **Authorized JavaScript origins**:
       ```
       http://localhost:3000
       http://localhost:3001
       http://localhost:3002
       ```
       (Add the port(s) you're using)
     
     - **Authorized redirect URIs**:
       ```
       http://localhost:3000/api/auth/callback/google
       http://localhost:3001/api/auth/callback/google
       http://localhost:3002/api/auth/callback/google
       ```
       (Add the port(s) you're using)
     
     - Click **Create**

5. **Copy Your Credentials**
   - A popup will show your **Client ID** and **Client Secret**
   - **Client ID** looks like: `123456789-abcdefghijklmnop.apps.googleusercontent.com`
   - **Client Secret** looks like: `GOCSPX-abcdefghijklmnopqrstuvwxyz`
   - **Copy both immediately** (you can't see the secret again)

### Step 3: Add Credentials to `.env.local`

1. **Create or Edit `.env.local`** in the `frontend/` directory:

```bash
cd frontend
nano .env.local
# or use your preferred editor
```

2. **Add the credentials** (replace with your actual values):

```env
GOOGLE_CLIENT_ID=123456789-abcdefghijklmnop.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-abcdefghijklmnopqrstuvwxyz

# Also make sure these are set:
DATABASE_URL=your-database-url
BETTER_AUTH_SECRET=your-32-character-secret
BETTER_AUTH_URL=http://localhost:3001
```

**Important Notes:**
- No quotes around the values
- No spaces around the `=` sign
- The Client ID should end with `.apps.googleusercontent.com`
- The Client Secret should start with `GOCSPX-`

### Step 4: Restart Your Development Server

```bash
# Stop your server (Ctrl+C)
# Then restart
cd frontend
npm run dev
```

### Step 5: Verify the Credentials Are Loaded

Check the server logs when it starts. You should see the app starting without errors about missing credentials.

### Step 6: Try Google Login Again

1. Clear your browser cache/cookies for localhost
2. Try logging in with Google again
3. The "invalid_client" error should be resolved

## Common Issues

### Issue: "The OAuth client was not found" after adding credentials

**Possible causes:**
1. **Wrong Client ID**: Double-check the Client ID matches exactly what's in Google Cloud Console
2. **Client ID format**: Should end with `.apps.googleusercontent.com`
3. **Environment variable not loaded**: Make sure you restarted the dev server after adding to `.env.local`
4. **Typo in variable name**: Should be exactly `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET`
5. **Wrong project**: Make sure you're using credentials from the correct Google Cloud project

**Solutions:**
- Verify the Client ID in Google Cloud Console → Credentials
- Check `.env.local` file is in the correct location (`frontend/.env.local`)
- Ensure no extra spaces or quotes in `.env.local`
- Restart the dev server completely

### Issue: Client Secret doesn't work

**Note**: If you lost your Client Secret, you'll need to:
1. Go to Google Cloud Console → Credentials
2. Edit your OAuth 2.0 Client ID
3. Generate a new client secret
4. Update `.env.local` with the new secret
5. Restart your dev server

### Issue: "redirect_uri_mismatch" error

This is different from "invalid_client". It means the redirect URI doesn't match. See `GOOGLE_OAUTH_FIX.md` for help with redirect URI configuration.

## Quick Checklist

- [ ] Created a Google Cloud Project
- [ ] Enabled necessary APIs (Google+ API or Google Identity)
- [ ] Configured OAuth consent screen
- [ ] Created OAuth 2.0 Client ID (Web application type)
- [ ] Added authorized JavaScript origins (localhost:3000, 3001, etc.)
- [ ] Added authorized redirect URIs (with `/api/auth/callback/google` path)
- [ ] Copied Client ID and Client Secret
- [ ] Created `frontend/.env.local` file
- [ ] Added `GOOGLE_CLIENT_ID=...` to `.env.local`
- [ ] Added `GOOGLE_CLIENT_SECRET=...` to `.env.local`
- [ ] Verified no quotes or extra spaces in `.env.local`
- [ ] Restarted dev server
- [ ] Cleared browser cache
- [ ] Tested Google login again

## Getting Your Credentials Again

If you need to view your credentials:

1. Go to: https://console.cloud.google.com → APIs & Services → Credentials
2. Find your OAuth 2.0 Client ID
3. Click the edit (pencil) icon
4. The Client ID is visible (you can copy it)
5. The Client Secret is masked - if you need a new one:
   - Click "RESET SECRET" (this invalidates the old one)
   - Copy the new secret immediately
   - Update `.env.local` with the new secret

## Still Having Issues?

1. **Check server logs** for any error messages about missing credentials
2. **Verify the file location**: `.env.local` must be in the `frontend/` directory (same level as `package.json`)
3. **Check for typos**: Variable names are case-sensitive
4. **Verify Google Cloud Console**: Make sure the OAuth client exists and is enabled
5. **Try creating a new OAuth client** if the current one seems corrupted

The most common issue is that the environment variables aren't being loaded. Make sure:
- The file is named exactly `.env.local` (starts with a dot)
- It's in the `frontend/` directory
- You restarted the dev server after adding/modifying it

