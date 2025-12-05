# Quick Fix: Backend Not Running

## The Problem
You're seeing "Failed to initialize. Make sure the backend is running." This means the frontend can't connect to the backend API.

## Solution: Start the Backend

### Option 1: Quick Start (Recommended)

Open a terminal in the project directory and run:

```bash
python backend/app.py
```

You should see:
```
Starting Book Recommendation Engine API...
Backend will be available at http://localhost:5000
Loading data and building recommendation engine...
Engine ready!
 * Running on http://0.0.0.0:5000
```

**Keep this terminal open!** The backend needs to keep running.

### Option 2: Use the Start Script

```bash
./start.sh
```

This starts both backend and frontend automatically.

## Verify Backend is Running

Open a new terminal and test:

```bash
curl http://localhost:5000/api/health
```

You should see: `{"status":"ok"}`

## Then Refresh Your Browser

Once the backend is running, refresh your browser page (http://localhost:3000) and it should work!

## Common Issues

### Port 5000 Already in Use

If you get an error about port 5000 being in use:

```bash
# Find what's using port 5000
lsof -ti:5000

# Kill it (replace PID with the number from above)
kill -9 <PID>
```

### Missing Dependencies

If you get import errors:

```bash
pip install -r requirements.txt
```

### CSV File Not Found

Make sure `goodreads_books_2024.csv` is in the project root directory.

