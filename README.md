# Book Recommendation Engine

A production-ready book recommendation engine with a modern React + TypeScript frontend and Python Flask backend. Uses efficient data loading, content-based, popularity-based, and hybrid recommendation strategies.

## Features

- **Efficient Data Loading**: Optimized memory usage with selective column loading and dtype optimization
- **Multiple Recommendation Strategies**: Content-based, popularity-based, and hybrid approaches
- **Strategy Pattern**: Clean, extensible design for easy algorithm swapping
- **Modern Web UI**: React + TypeScript frontend with responsive design
- **RESTful API**: Flask backend with CORS support
- **Performance Optimized**: Vectorized operations and pre-computed similarity matrices

## Project Structure

```
Book-Recommendation-Engine/
├── backend/
│   └── app.py              # Flask API server
├── frontend/
│   ├── src/
│   │   ├── App.tsx         # Main React component
│   │   ├── App.css         # Styles
│   │   ├── api.ts          # API client
│   │   ├── types.ts        # TypeScript types
│   │   ├── main.tsx        # Entry point
│   │   └── index.css       # Global styles
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
├── data_loader.py          # Efficient data loading and preprocessing
├── book_recommender.py     # Recommendation engine with Strategy pattern
├── demo.py                 # Command-line demonstration
├── requirements.txt        # Python dependencies
├── start.sh               # Start script for both servers
└── README.md              # This file
```

## Prerequisites

- Python 3.8+
- Node.js 16+ and npm
- The Goodreads dataset CSV file

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install Frontend Dependencies

```bash
cd frontend
npm install
cd ..
```

### 3. Download Dataset

Download the Goodreads Books Dataset (May 2024) from [Kaggle](https://www.kaggle.com/datasets/dk123891/books-dataset-goodreadsmay-2024) and place it as `goodreads_books_2024.csv` in the project root directory.

## Usage

### Quick Start (Recommended)

Use the start script to run both servers:

```bash
./start.sh
```

This will:

1. Start the backend API on http://localhost:5000
2. Start the frontend dev server on http://localhost:3000
3. Open the UI in your browser

### Manual Start

**Terminal 1 - Backend:**

```bash
python backend/app.py
```

**Terminal 2 - Frontend:**

```bash
cd frontend
npm run dev
```

### Command Line Demo

Run the comprehensive demo script:

```bash
python demo.py
```

## API Endpoints

The backend provides the following REST API endpoints:

- `GET /api/health` - Health check
- `GET /api/stats` - Get dataset statistics

  ```json
  {
    "total_books": 16225,
    "memory_mb": 4.45,
    "average_rating": 4.12,
    "total_ratings": 123456789,
    "unique_authors": 5432,
    "avg_pages": 350
  }
  ```

- `GET /api/search?q=<query>&limit=<n>` - Search for books

  ```json
  {
    "books": [
      {
        "id": 1,
        "title": "Book Title",
        "author": "Author Name",
        "rating": 4.5,
        "num_ratings": 1000,
        "genres": ["Fantasy", "Fiction"]
      }
    ]
  }
  ```

- `GET /api/popular?limit=<n>` - Get popular books

  ```json
  {
    "books": [...]
  }
  ```

- `POST /api/recommendations` - Get book recommendations

  ```json
  Request:
  {
    "book_title": "Harry Potter",
    "strategy": "hybrid",
    "n": 5
  }

  Response:
  {
    "recommendations": [
      {
        "id": 1,
        "title": "Recommended Book",
        "author": "Author",
        "rating": 4.5,
        "num_ratings": 1000,
        "genres": ["Fantasy"],
        "score": 0.95
      }
    ]
  }
  ```

## Recommendation Strategies

1. **Content-Based**: Recommends books similar in features (genres, ratings, pages)
2. **Popularity-Based**: Recommends top-rated books
3. **Hybrid**: Combines content similarity (70%) with popularity (30%)

## Frontend Features

- **Book Search**: Real-time search with autocomplete
- **Strategy Selection**: Switch between recommendation strategies
- **Recommendation Display**: Beautiful card-based layout
- **Popular Books**: Sidebar with top-rated books
- **Statistics Dashboard**: Dataset metrics and performance stats
- **Responsive Design**: Works on desktop and mobile

## Performance

- **Data Loading**: ~0.4 seconds for 16K+ books
- **Engine Build**: ~13 seconds (one-time similarity matrix computation)
- **Recommendation Query**: ~0.007 seconds average
- **Memory Usage**: ~4.5 MB for optimized dataset

## Technologies

- **Backend**: Python, Flask, pandas, NumPy, scikit-learn
- **Frontend**: React, TypeScript, Vite
- **Architecture**: RESTful API with Strategy pattern

## Development

### Backend Development

The backend uses Flask with CORS enabled. The recommendation engine is initialized on first request and cached for subsequent requests.

### Frontend Development

The frontend uses Vite for fast development. The API client (`src/api.ts`) handles all backend communication with proper TypeScript types.

## Troubleshooting

### Backend Issues

- Ensure the CSV file is in the project root
- Check that all Python dependencies are installed
- Verify port 5000 is not in use
- Check `backend.log` for error messages

### Frontend Issues

- Run `npm install` in the frontend directory
- Check that port 3000 is not in use
- Verify the backend is running before starting the frontend
- Check browser console for errors

### CORS Issues

The backend has CORS enabled. If you encounter issues, ensure `flask-cors` is installed.

## License

See LICENSE file for details.
