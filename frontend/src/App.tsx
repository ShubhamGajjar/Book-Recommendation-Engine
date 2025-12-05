import { useState, useEffect } from 'react'
import { api } from './api'
import type { Book, Stats } from './types'
import './App.css'

function App() {
  const [bookTitle, setBookTitle] = useState('')
  const [strategy, setStrategy] = useState<'hybrid' | 'content' | 'popularity'>('hybrid')
  const [numRecs, setNumRecs] = useState(5)
  const [recommendations, setRecommendations] = useState<Book[]>([])
  const [popularBooks, setPopularBooks] = useState<Book[]>([])
  const [stats, setStats] = useState<Stats | null>(null)
  const [searchQuery, setSearchQuery] = useState('')
  const [searchResults, setSearchResults] = useState<Book[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [initializing, setInitializing] = useState(true)

  useEffect(() => {
    const initialize = async () => {
      try {
        // First check if backend is reachable
        const healthCheck = await fetch('/api/health').catch(() => null)
        if (!healthCheck || !healthCheck.ok) {
          throw new Error('Backend server is not responding. Please start the backend server.')
        }

        const [statsData, popularData] = await Promise.all([
          api.getStats(),
          api.getPopularBooks(5)
        ])
        setStats(statsData)
        setPopularBooks(popularData)
      } catch (err) {
        console.error('Initialization error:', err)
        const errorMessage = err instanceof Error 
          ? err.message 
          : 'Failed to initialize. Make sure the backend is running on http://localhost:5000'
        setError(errorMessage)
      } finally {
        setInitializing(false)
      }
    }
    initialize()
  }, [])

  useEffect(() => {
    if (searchQuery.length < 2) {
      setSearchResults([])
      return
    }

    const timeoutId = setTimeout(async () => {
      try {
        const results = await api.searchBooks(searchQuery, 10)
        setSearchResults(results)
      } catch (err) {
        console.error('Search error:', err)
        setSearchResults([])
      }
    }, 300)

    return () => clearTimeout(timeoutId)
  }, [searchQuery])

  const handleGetRecommendations = async () => {
    const trimmedTitle = bookTitle.trim()
    if (!trimmedTitle) {
      setError('Please enter a book title')
      return
    }

    setLoading(true)
    setError('')

    try {
      const results = await api.getRecommendations({
        book_title: trimmedTitle,
        strategy,
        n: numRecs,
      })
      setRecommendations(results)
      if (results.length === 0) {
        setError('No recommendations found. Try a different book title.')
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
      setRecommendations([])
    } finally {
      setLoading(false)
    }
  }

  const handleBookTitleChange = (value: string) => {
    setBookTitle(value)
    if (error) {
      setError('')
    }
  }

  const handleSelectBook = (title: string) => {
    setBookTitle(title)
    setSearchQuery('')
    setSearchResults([])
  }

  if (initializing) {
    return (
      <div className="app">
        <div className="loading-screen">
          <div style={{ 
            fontSize: '4rem', 
            marginBottom: '20px',
            animation: 'pulse 2s ease-in-out infinite'
          }}>📚</div>
          <h1>Book Recommendation Engine</h1>
          <p style={{ marginTop: '15px' }}>Loading...</p>
          <div style={{ 
            marginTop: '20px',
            width: '50px',
            height: '50px',
            border: '4px solid rgba(255,255,255,0.3)',
            borderTop: '4px solid white',
            borderRadius: '50%',
            animation: 'spin 1s linear infinite'
          }}></div>
          <p style={{ fontSize: '0.9rem', marginTop: '20px', opacity: 0.8 }}>
            Connecting to backend server...
          </p>
        </div>
        <style>{`
          @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
          }
        `}</style>
      </div>
    )
  }

  if (error && !stats) {
    return (
      <div className="app">
        <div className="loading-screen">
          <h1>📚 Book Recommendation Engine</h1>
          <div className="error-container">
            <p style={{ color: '#c33', marginBottom: '20px' }}>⚠️ {error}</p>
            <div style={{ textAlign: 'left', background: 'white', padding: '20px', borderRadius: '8px', maxWidth: '600px' }}>
              <h3 style={{ marginBottom: '15px' }}>To start the backend:</h3>
              <ol style={{ lineHeight: '1.8' }}>
                <li>Open a terminal in the project directory</li>
                <li>Run: <code style={{ background: '#f0f0f0', padding: '2px 6px', borderRadius: '4px' }}>python backend/app.py</code></li>
                <li>Wait for "Engine ready!" message</li>
                <li>Refresh this page</li>
              </ol>
              <p style={{ marginTop: '15px', fontSize: '0.9rem', color: '#666' }}>
                Or use the start script: <code style={{ background: '#f0f0f0', padding: '2px 6px', borderRadius: '4px' }}>./start.sh</code>
              </p>
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="app">
      <header className="header">
        <h1>📚 Book Recommendation Engine</h1>
        <p>Discover your next favorite book using AI-powered recommendations</p>
      </header>

      <div className="container">
        <aside className="sidebar">
          <div className="sidebar-section">
            <h2>⚙️ Settings</h2>
            <div className="form-group">
              <label>Strategy</label>
              <select value={strategy} onChange={(e) => setStrategy(e.target.value as any)}>
                <option value="hybrid">Hybrid</option>
                <option value="content">Content-Based</option>
                <option value="popularity">Popularity</option>
              </select>
              <small>Hybrid combines content similarity with popularity</small>
            </div>
            <div className="form-group">
              <label>Number of Recommendations: {numRecs}</label>
              <input
                type="range"
                min="3"
                max="20"
                value={numRecs}
                onChange={(e) => setNumRecs(Number(e.target.value))}
              />
            </div>
          </div>

          <div className="sidebar-section">
            <h2>🔍 Quick Search</h2>
            <input
              type="text"
              placeholder="Search books..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="search-input"
            />
            {searchResults.length > 0 && (
              <div className="search-results">
                {searchResults.map((book) => (
                  <button
                    key={book.id}
                    className="search-result-item"
                    onClick={() => handleSelectBook(book.title)}
                  >
                    <div className="search-result-title">{book.title}</div>
                    <div className="search-result-author">{book.author}</div>
                  </button>
                ))}
              </div>
            )}
          </div>

          {stats && (
            <div className="sidebar-section">
              <h2>📊 Statistics</h2>
              <div className="stat-item">
                <span>Total Books</span>
                <strong>{stats.total_books.toLocaleString()}</strong>
              </div>
              <div className="stat-item">
                <span>Memory Usage</span>
                <strong>{stats.memory_mb} MB</strong>
              </div>
              <div className="stat-item">
                <span>Avg Rating</span>
                <strong>{stats.average_rating} ⭐</strong>
              </div>
              <div className="stat-item">
                <span>Total Ratings</span>
                <strong>{stats.total_ratings.toLocaleString()}</strong>
              </div>
            </div>
          )}
        </aside>

        <main className="main-content">
          <div className="search-section">
            <h2>🔍 Find Recommendations</h2>
            <p className="section-hint">Enter a book title below to get personalized recommendations</p>
            <div className="input-group">
              <input
                type="text"
                placeholder="Enter a book title (e.g., Harry Potter and the Half-Blood Prince)"
                value={bookTitle}
                onChange={(e) => handleBookTitleChange(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleGetRecommendations()}
                className="book-input"
                disabled={loading}
              />
              <button
                onClick={handleGetRecommendations}
                disabled={loading || !bookTitle.trim()}
                className="btn-primary"
              >
                {loading ? 'Loading...' : 'Get Recommendations'}
              </button>
            </div>
            {error && <div className="error-message">{error}</div>}
            {!bookTitle && !error && (
              <div className="help-text">
                💡 Tip: Try searching for popular books like "Harry Potter", "1984", or "The Great Gatsby"
              </div>
            )}
          </div>

          {recommendations.length > 0 && (
            <div className="recommendations-section">
              <h2>📖 Recommendations</h2>
              <div className="recommendations-grid">
                {recommendations.map((book, index) => (
                  <div key={book.id} className="book-card">
                    <div className="book-rank">#{index + 1}</div>
                    <h3 className="book-title">{book.title}</h3>
                    <p className="book-author">by {book.author}</p>
                    <div className="book-genres">
                      {book.genres.map((genre, i) => (
                        <span key={i} className="genre-tag">
                          {genre}
                        </span>
                      ))}
                    </div>
                    <div className="book-metrics">
                      <div className="metric">
                        <span className="metric-label">Rating</span>
                        <span className="metric-value">{book.rating.toFixed(2)} ⭐</span>
                      </div>
                      <div className="metric">
                        <span className="metric-label">Ratings</span>
                        <span className="metric-value">{book.num_ratings.toLocaleString()}</span>
                      </div>
                      {book.score !== undefined && (
                        <div className="metric">
                          <span className="metric-label">Match</span>
                          <span className="metric-value">{book.score.toFixed(3)}</span>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          <div className="popular-section">
            <h2>📈 Popular Books</h2>
            <div className="popular-list">
              {popularBooks.map((book, index) => (
                <div key={book.id} className="popular-item">
                  <div className="popular-rank">{index + 1}</div>
                  <div className="popular-info">
                    <h4>{book.title}</h4>
                    <p>{book.author}</p>
                    <div className="popular-meta">
                      <span>⭐ {book.rating.toFixed(2)}</span>
                      <span>📊 {book.num_ratings.toLocaleString()} ratings</span>
                    </div>
                  </div>
                  <button
                    className="btn-small"
                    onClick={() => handleSelectBook(book.title)}
                  >
                    Get Similar
                  </button>
                </div>
              ))}
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}

export default App
