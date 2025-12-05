# Fix: Port 5000 Already in Use

## Quick Fix (Recommended)

I've updated the code to automatically use port 5001 instead. Just restart the backend:

```bash
python backend/app.py
```

The backend will now automatically find a free port (starting from 5001) and the frontend is configured to connect to it.

## Alternative: Free Up Port 5000

If you want to use port 5000, you can free it up:

### Option 1: Disable AirPlay Receiver (macOS)

1. Open **System Preferences** (or **System Settings** on newer macOS)
2. Go to **General** → **AirDrop & Handoff**
3. Turn off **AirPlay Receiver**
4. Restart the backend

### Option 2: Kill the Process Using Port 5000

```bash
# Find the process
lsof -ti:5000

# Kill it (replace PID with the number from above)
kill -9 <PID>
```

Or in one command:
```bash
lsof -ti:5000 | xargs kill -9
```

## Verify

After starting the backend, you should see:
```
Backend will be available at http://localhost:5001
```

Then refresh your browser - it should work!

