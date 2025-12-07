# Fixing JWT 401 Unauthorized After Secret Update

## Problem
After updating `BETTER_AUTH_SECRET` to match between frontend and backend, you're still getting 401 errors.

## Solution: Force Backend to Reload Settings

The backend caches settings. Follow these steps to ensure it picks up the new secret:

### Step 1: Verify the Secret Matches

**Check frontend:**
```bash
cd frontend
grep BETTER_AUTH_SECRET .env.local
```

**Check backend:**
```bash
cd backend
grep BETTER_AUTH_SECRET .env
```

Both should show the **exact same value**.

### Step 2: Completely Stop and Restart Backend

**Important**: You need to **completely stop** the backend, not just reload:

1. **Stop the backend** (in the terminal where it's running):
   - Press `Ctrl+C` to stop
   - Wait for it to fully stop
   - Make sure the process is completely terminated

2. **Verify it's stopped:**
   ```bash
   curl http://localhost:8000/health
   # Should fail with "Connection refused"
   ```

3. **Start it again:**
   ```bash
   cd backend
   uv run uvicorn src.api.main:app --reload --port 8000
   ```

4. **Check the startup logs** - you should see:
   ```
   ✅ Loaded settings - BETTER_AUTH_SECRET: JU1I9zfPxGQAoOoeD+... (length: 44)
   ```

### Step 3: Check Environment Variables Aren't Overriding

If you're running the backend with environment variables set in your shell, they might override the `.env` file:

```bash
# Check if BETTER_AUTH_SECRET is set in your shell
echo $BETTER_AUTH_SECRET

# If it shows the OLD secret, unset it:
unset BETTER_AUTH_SECRET

# Then restart the backend
```

### Step 4: Clear Browser Data and Test

1. **Clear browser cookies** for localhost:
   - DevTools (F12) → Application → Cookies → Clear all
   
2. **Log in again** with Google

3. **Try loading tasks** - should work now!

## Verification

After restarting, check the backend logs when you try to access tasks:

**If it works**, you'll see:
```
INFO:     127.0.0.1:xxxxx - "GET /api/tasks/ HTTP/1.1" 200 OK
```

**If it still fails**, you'll see:
```
⚠️  JWT validation failed: ...
⚠️  Using secret: ...
```

Compare the secret in the logs with your frontend secret - they must match exactly.

## Alternative: Set Secret as Environment Variable

If the `.env` file isn't being read, you can set it directly when starting:

```bash
cd backend
BETTER_AUTH_SECRET="JU1I9zfPxGQAoOoeD+J/GWr0tyR3Zs4cO5kfQdmz/0E=" uv run uvicorn src.api.main:app --reload --port 8000
```

## Still Having Issues?

1. **Check the actual secret being used:**
   - Look at backend startup logs for the "Loaded settings" message
   - Compare it character-by-character with frontend secret
   - Make sure there are no extra spaces or newlines

2. **Test JWT generation manually:**
   - In browser console after logging in:
   ```javascript
   fetch('/api/auth/token', {credentials: 'include'})
     .then(r => r.json())
     .then(d => {
       console.log('Token:', d.token);
       // Decode the token (just to see payload, not validate)
       const payload = JSON.parse(atob(d.token.split('.')[1]));
       console.log('Payload:', payload);
     })
   ```

3. **Test backend validation:**
   ```bash
   # Get token from browser console first
   TOKEN="your-token-here"
   
   # Test with backend
   curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/tasks/
   ```

The key is: **Both frontend and backend must use the EXACT same secret string**.

