from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from data_loader import BookDataLoader
from book_recommender import BookRecommendationEngine

app = Flask(__name__)
CORS(app)

loader = None
engine = None
books_df = None

def init_engine():
    global loader, engine, books_df
    if engine is None:
        print("Loading data and building recommendation engine...")
        csv_path = os.path.join(parent_dir, "goodreads_books_2024.csv")
        loader = BookDataLoader(csv_path)
        books_df = loader.load_and_preprocess()
        engine = BookRecommendationEngine(books_df)
        print("Engine ready!")

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

@app.route('/api/stats', methods=['GET'])
def get_stats():
    if books_df is None:
        init_engine()
    
    memory_info = loader.get_memory_usage()
    
    return jsonify({
        "total_books": len(books_df),
        "memory_mb": round(memory_info['total_memory_mb'], 2),
        "average_rating": round(float(books_df['average_rating'].mean()), 2),
        "total_ratings": int(books_df['num_ratings'].sum()),
        "unique_authors": int(books_df['author'].nunique()),
        "avg_pages": int(books_df['num_pages'].mean())
    })

@app.route('/api/search', methods=['GET'])
def search_books():
    if books_df is None:
        init_engine()
    
    query = request.args.get('q', '').strip()
    limit = int(request.args.get('limit', 10))
    
    if not query:
        return jsonify({"books": []})
    
    matches = books_df[
        books_df['book_title'].str.contains(query, case=False, na=False)
    ].head(limit)
    
    books = []
    for idx, row in matches.iterrows():
        books.append({
            "id": int(idx),
            "title": row['book_title'],
            "author": row['author'],
            "rating": float(row['average_rating']),
            "num_ratings": int(row['num_ratings']),
            "genres": row['genres'][:3] if isinstance(row['genres'], list) and row['genres'] else []
        })
    
    return jsonify({"books": books})

@app.route('/api/popular', methods=['GET'])
def get_popular():
    if books_df is None:
        init_engine()
    
    limit = int(request.args.get('limit', 5))
    top_books = books_df.nlargest(limit, 'popularity_score')
    
    books = []
    for idx, row in top_books.iterrows():
        books.append({
            "id": int(idx),
            "title": row['book_title'],
            "author": row['author'],
            "rating": float(row['average_rating']),
            "num_ratings": int(row['num_ratings']),
            "genres": row['genres'][:3] if isinstance(row['genres'], list) and row['genres'] else [],
            "popularity_score": float(row['popularity_score'])
        })
    
    return jsonify({"books": books})

@app.route('/api/recommendations', methods=['POST'])
def get_recommendations():
    if engine is None:
        init_engine()
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body is required"}), 400
        
        book_title = data.get('book_title', '').strip()
        strategy = data.get('strategy', 'hybrid')
        n = int(data.get('n', 5))
        
        if not book_title:
            return jsonify({"error": "book_title is required"}), 400
        
        if strategy not in ['hybrid', 'content', 'popularity']:
            return jsonify({"error": "strategy must be one of: hybrid, content, popularity"}), 400
        
        if n < 1 or n > 50:
            return jsonify({"error": "n must be between 1 and 50"}), 400
        
        recommendations = engine.get_recommendations(book_title, strategy=strategy, n=n)
        
        if not recommendations:
            return jsonify({"error": "Book not found in dataset"}), 404
        
        recs = []
        for book_id, title, score in recommendations:
            book = books_df.loc[book_id]
            recs.append({
                "id": int(book_id),
                "title": title,
                "author": book['author'],
                "rating": float(book['average_rating']),
                "num_ratings": int(book['num_ratings']),
                "genres": book['genres'][:3] if isinstance(book['genres'], list) and book['genres'] else [],
                "score": round(float(score), 3)
            })
        
        return jsonify({"recommendations": recs})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting Book Recommendation Engine API...")
    print("Backend will be available at http://localhost:5001")
    print("(Using port 5001 to avoid conflict with macOS AirPlay Receiver on port 5000)")
    init_engine()
    app.run(debug=True, port=5001, host='0.0.0.0')
