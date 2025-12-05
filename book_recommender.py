import pandas as pd
import numpy as np
from typing import List, Tuple
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MultiLabelBinarizer
import re


def normalize_title(title: str) -> str:
    """Normalize book title for comparison (remove extra spaces, punctuation)."""
    if not isinstance(title, str):
        return ""
    normalized = re.sub(r'[^\w\s]', '', title.lower())
    normalized = re.sub(r'\s+', ' ', normalized).strip()
    return normalized


def deduplicate_recommendations(recommendations: List[Tuple[int, str, float]], 
                                books_df: pd.DataFrame, 
                                n: int) -> List[Tuple[int, str, float]]:
    """Remove duplicate books based on normalized title and author."""
    seen = set()
    unique_recs = []
    
    for book_id, title, score in recommendations:
        try:
            book = books_df.loc[book_id]
            author = str(book['author']).lower().strip() if pd.notna(book['author']) else ""
            normalized_title = normalize_title(title)
            
            key = (normalized_title, author)
            
            if key not in seen:
                seen.add(key)
                unique_recs.append((book_id, title, score))
                
                if len(unique_recs) >= n:
                    break
        except (KeyError, IndexError):
            continue
    
    return unique_recs


class RecommendationStrategy:
    def recommend(self, book_id: int, n: int = 5) -> List[Tuple[int, str, float]]:
        raise NotImplementedError("Subclasses must implement recommend()")


class ContentBasedRecommender(RecommendationStrategy):
    def __init__(self, books_df: pd.DataFrame):
        self.books_df = books_df.copy()
        self.similarity_matrix = None
        self._prepare_features()

    def _prepare_features(self):
        mlb = MultiLabelBinarizer()
        genre_features = mlb.fit_transform(self.books_df['genres'])

        max_pages = self.books_df['num_pages'].max()
        if max_pages > 0:
            normalized_pages = (self.books_df['num_pages'] / max_pages).values.reshape(-1, 1)
        else:
            normalized_pages = np.zeros((len(self.books_df), 1))

        normalized_rating = (self.books_df['average_rating'] / 5.0).values.reshape(-1, 1)

        self.feature_matrix = np.hstack([
            genre_features,
            normalized_pages,
            normalized_rating
        ])

        self._compute_similarity_matrix()

    def _compute_similarity_matrix(self):
        self.similarity_matrix = cosine_similarity(self.feature_matrix)

    def recommend(self, book_id: int, n: int = 5) -> List[Tuple[int, str, float]]:
        try:
            idx = self.books_df.index.get_loc(book_id)
        except (KeyError, IndexError):
            return []

        sim_scores = self.similarity_matrix[idx]
        similar_indices = np.argsort(sim_scores)[::-1][1:n * 3 + 1]

        recommendations = []
        for similar_idx in similar_indices:
            book_row = self.books_df.iloc[similar_idx]
            recommendations.append((
                self.books_df.index[similar_idx],
                book_row['book_title'],
                float(sim_scores[similar_idx])
            ))

        return deduplicate_recommendations(recommendations, self.books_df, n)


class PopularityRecommender(RecommendationStrategy):
    def __init__(self, books_df: pd.DataFrame):
        self.books_df = books_df.copy()

    def recommend(self, book_id: int = None, genre: str = None, n: int = 5) -> List[Tuple[int, str, float]]:
        df = self.books_df.copy()

        if genre:
            df = df[df['genres'].apply(lambda x: genre in x if isinstance(x, list) else False)]

        top_books = df.nlargest(n * 3, 'popularity_score')

        recommendations = []
        for idx, row in top_books.iterrows():
            recommendations.append((
                idx,
                row['book_title'],
                row['popularity_score']
            ))

        return deduplicate_recommendations(recommendations, self.books_df, n)


class HybridRecommender(RecommendationStrategy):
    def __init__(self, books_df: pd.DataFrame,
                 content_weight: float = 0.7,
                 popularity_weight: float = 0.3):
        self.content_recommender = ContentBasedRecommender(books_df)
        self.popularity_recommender = PopularityRecommender(books_df)
        self.books_df = books_df
        self.content_weight = content_weight
        self.popularity_weight = popularity_weight

    def recommend(self, book_id: int, n: int = 5) -> List[Tuple[int, str, float]]:
        content_recs = self.content_recommender.recommend(book_id, n * 3)
        
        if not content_recs:
            return []

        content_scores = {bid: score for bid, _, score in content_recs}
        candidate_ids = [bid for bid, _, _ in content_recs]
        candidate_books = self.books_df[self.books_df.index.isin(candidate_ids)]

        if candidate_books.empty:
            return []

        max_pop = candidate_books['popularity_score'].max()
        if max_pop == 0:
            max_pop = 1.0

        combined_scores = []
        for idx, row in candidate_books.iterrows():
            content_score = content_scores.get(idx, 0.0)
            popularity_score = row['popularity_score'] / max_pop

            combined = (self.content_weight * content_score +
                       self.popularity_weight * popularity_score)

            combined_scores.append((
                idx,
                row['book_title'],
                combined
            ))

        combined_scores.sort(key=lambda x: x[2], reverse=True)
        return deduplicate_recommendations(combined_scores, self.books_df, n)


class BookRecommendationEngine:
    def __init__(self, books_df: pd.DataFrame):
        self.books_df = books_df
        self.strategies = {
            'content': ContentBasedRecommender(books_df),
            'popularity': PopularityRecommender(books_df),
            'hybrid': HybridRecommender(books_df)
        }

    def get_recommendations(self,
                            book_title: str,
                            strategy: str = 'hybrid',
                            n: int = 5) -> List[Tuple[int, str, float]]:
        matches = self.books_df[
            self.books_df['book_title'].str.contains(book_title, case=False, na=False)
        ]

        if matches.empty:
            return []

        book_id = matches.index[0]

        if strategy not in self.strategies:
            raise ValueError(f"Unknown strategy: {strategy}")

        return self.strategies[strategy].recommend(book_id, n)

    def display_recommendations(self, recommendations: List[Tuple[int, str, float]]):
        if not recommendations:
            print("No recommendations found.")
            return

        print("\n" + "=" * 80)
        print("RECOMMENDATIONS")
        print("=" * 80)

        for i, (book_id, title, score) in enumerate(recommendations, 1):
            book = self.books_df.loc[book_id]
            genres_display = ', '.join(book['genres'][:3]) if book['genres'] else 'N/A'

            print(f"\n{i}. {title}")
            print(f"   Author: {book['author']}")
            print(f"   Rating: {book['average_rating']:.2f} ⭐ ({book['num_ratings']:,} ratings)")
            print(f"   Genres: {genres_display}")
            print(f"   Match Score: {score:.3f}")

        print("\n" + "=" * 80)


if __name__ == "__main__":
    from data_loader import BookDataLoader

    print("Loading data...")
    loader = BookDataLoader("goodreads_books_2024.csv")
    books_df = loader.load_and_preprocess()

    print("Building recommendation engine...")
    engine = BookRecommendationEngine(books_df)

    test_book = "Harry Potter"
    print(f"\nGetting recommendations for books like '{test_book}'...")

    for strategy in ['content', 'popularity', 'hybrid']:
        print(f"\n{'=' * 80}")
        print(f"Strategy: {strategy.upper()}")
        print('=' * 80)

        recommendations = engine.get_recommendations(test_book, strategy=strategy, n=5)
        engine.display_recommendations(recommendations)

