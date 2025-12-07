# Debugging Railway Container Stop Issue

## Problem Analysis

**Symptoms:**
- ✅ App starts successfully
- ✅ Healthcheck passes (200 OK)
- ✅ Database initializes
- ❌ Container stops after ~2 seconds
- ❌ Railway shows "Stopping Container"

**Key Insight:** Railway is explicitly stopping the container, not the app crashing.

## Debugging Steps

### 1. Check Port Configuration

**The Issue:** Logs show app running on port 8080, but Railway might expect a different port.

**Check in Railway Dashboard:**
1. Railway → Service → Settings
2. Look for **"Port"** or **"Target Port"** setting
3. This should match the port your app listens on

**What to verify:**
- Railway might have a "Target Port" setting that needs to match
- If set to 8000 but app runs on 8080, Railway will stop the container
- Or vice versa

### 2. Check Railway Service Settings

In Railway → Service → Settings, look for:

**A. Port/Target Port Setting:**
- Should match the port your app uses
- If Railway expects 8000 but app uses 8080, there's a mismatch

**B. Healthcheck Configuration:**
- Healthcheck Path: `/health`
- Healthcheck Timeout: Should be 300 (we set this)
- Check if there's a "Healthcheck Port" setting

**C. Service Type:**
- Should be "Web Service" (not "Job" or "Cron")
- If it's a Job, it will stop after completion

### 3. Add Debug Logging

I've added debug logging to show what port Railway is setting. After redeploy, check logs for:
```
🔍 DEBUG: PORT environment variable = ???
```

This will show what Railway is actually setting.

### 4. Check Railway's Internal Port Check

Railway might be doing a TCP port check (not just HTTP healthcheck). If the app isn't listening on the port Railway expects, it stops the container.

**Test:**
- Check what port Railway expects
- Verify app is listening on that exact port

### 5. Check Service Settings for "Stop" Configuration

Look for any settings like:
- "Stop After" timeout
- "Auto-stop" settings
- "Idle timeout"
- Resource limits that might cause shutdown

### 6. Check Railway Service Status

Railway → Service → Overview:
- Is service status "Active" or "Stopped"?
- Is there a "Start" button (means it's stopped)?
- Check if there are any warnings or errors

## Most Likely Causes (Ranked)

1. **Port Mismatch** - Railway expects different port than app uses
2. **Service Type** - Configured as Job instead of Web Service
3. **Target Port Setting** - Railway has explicit port setting that doesn't match
4. **Healthcheck Port** - Railway checking wrong port for health
5. **Resource Limits** - Free tier limits causing shutdown

## Action Items

1. **Check Railway Settings → Port/Target Port**
   - What port does Railway expect?
   - Does it match what the app uses?

2. **Check Service Type**
   - Is it "Web Service" or something else?

3. **Redeploy with Debug Logging**
   - I've added port debugging
   - Check logs after redeploy to see what PORT is set to

4. **Check Railway Documentation**
   - Look for "target port" or "service port" settings
   - Verify healthcheck configuration

## Next Steps

1. Check Railway → Service → Settings for any port-related settings
2. Redeploy and check logs for the DEBUG messages
3. Compare the port in logs vs what Railway expects
4. If mismatch found, fix it

