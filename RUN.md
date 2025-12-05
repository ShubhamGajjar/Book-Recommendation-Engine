# How to Run the Book Recommendation Engine

## Quick Start (Easiest Method)

### Step 1: Install Dependencies

**Install Python dependencies:**
```bash
pip install -r requirements.txt
```

**Install Node.js dependencies:**
```bash
cd frontend
npm install
cd ..
```

### Step 2: Ensure Dataset is Available

Make sure `goodreads_books_2024.csv` is in the project root directory.

### Step 3: Run Everything

Use the start script:
```bash
./start.sh
```

This will automatically:
- Start the backend API on http://localhost:5000
- Start the frontend on http://localhost:3000
- Open the application in your browser

Press `Ctrl+C` to stop both servers.

---

## Manual Method (Two Terminals)

### Terminal 1 - Backend Server

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

### Terminal 2 - Frontend Server

```bash
cd frontend
npm run dev
```

You should see:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
```

### Open in Browser

Navigate to: **http://localhost:3000**

---

## Step-by-Step Setup (First Time)

### 1. Check Prerequisites

**Python:**
```bash
python --version
# Should be Python 3.8 or higher
```

**Node.js:**
```bash
node --version
# Should be Node.js 16 or higher
npm --version
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- pandas
- numpy
- scikit-learn
- flask
- flask-cors

### 3. Install Frontend Dependencies

```bash
cd frontend
npm install
cd ..
```

This installs:
- React
- TypeScript
- Vite
- And other frontend dependencies

### 4. Verify Dataset

Check that the CSV file exists:
```bash
ls -lh goodreads_books_2024.csv
```

If it doesn't exist, download it from [Kaggle](https://www.kaggle.com/datasets/dk123891/books-dataset-goodreadsmay-2024) and place it in the project root.

### 5. Run the Application

**Option A: Use start script**
```bash
./start.sh
```

**Option B: Run manually (two terminals)**
- Terminal 1: `python backend/app.py`
- Terminal 2: `cd frontend && npm run dev`

---

## Troubleshooting

### Backend Won't Start

**Error: Module not found**
```bash
pip install -r requirements.txt
```

**Error: Port 5000 already in use**
```bash
# Find and kill the process using port 5000
lsof -ti:5000 | xargs kill -9
```

**Error: CSV file not found**
- Make sure `goodreads_books_2024.csv` is in the project root
- Check the filename is exactly `goodreads_books_2024.csv`

### Frontend Won't Start

**Error: node_modules not found**
```bash
cd frontend
npm install
```

**Error: Port 3000 already in use**
```bash
# Find and kill the process using port 3000
lsof -ti:3000 | xargs kill -9
```

**Error: npm command not found**
- Install Node.js from https://nodejs.org/

### Application Loads But Shows Errors

**"Failed to initialize" error:**
- Make sure the backend is running on port 5000
- Check browser console for detailed error messages
- Verify CORS is enabled (should be automatic)

**No recommendations showing:**
- Check that the book title exists in the dataset
- Try searching for popular books like "Harry Potter"
- Check backend terminal for error messages

---

## Testing the API Directly

You can test the backend API directly using curl:

```bash
# Health check
curl http://localhost:5000/api/health

# Get statistics
curl http://localhost:5000/api/stats

# Search for books
curl "http://localhost:5000/api/search?q=Harry%20Potter&limit=5"

# Get popular books
curl http://localhost:5000/api/popular?limit=5

# Get recommendations
curl -X POST http://localhost:5000/api/recommendations \
  -H "Content-Type: application/json" \
  -d '{"book_title": "Harry Potter", "strategy": "hybrid", "n": 5}'
```

---

## Development Mode

### Backend (Auto-reload on changes)
The Flask backend runs in debug mode, so it will auto-reload when you change Python files.

### Frontend (Hot Module Replacement)
The Vite dev server supports hot module replacement, so changes to React components will update instantly in the browser.

---

## Production Build

### Build Frontend for Production

```bash
cd frontend
npm run build
```

This creates an optimized build in the `frontend/dist` directory.

### Serve Production Build

You can serve the production build using any static file server, or configure Flask to serve it.

---

## Need Help?

1. Check the README.md for more details
2. Check backend.log for backend errors (if using start.sh)
3. Check browser console for frontend errors
4. Verify all dependencies are installed correctly

