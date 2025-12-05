import pandas as pd
import numpy as np
from typing import List, Dict, Any
import ast


class BookDataLoader:
    COLUMNS_TO_LOAD = [
        'book_id',
        'book_title',
        'author',
        'genres',
        'num_ratings',
        'num_reviews',
        'average_rating',
        'num_pages'
    ]

    DTYPE_SPECIFICATION = {
        'book_id': 'int32',
        'book_title': 'string',
        'author': 'string',
        'num_ratings': 'int32',
        'num_reviews': 'int32',
        'average_rating': 'float32',
        'num_pages': 'string'
    }

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.data = None

    def load_data(self) -> pd.DataFrame:
        self.data = pd.read_csv(
            self.filepath,
            usecols=self.COLUMNS_TO_LOAD,
            dtype=self.DTYPE_SPECIFICATION,
            index_col=0
        )
        return self.data

    def preprocess_data(self) -> pd.DataFrame:
        if self.data is None:
            raise ValueError("Data not loaded. Call load_data() first.")

        self.data['genres'] = self.data['genres'].apply(self._parse_genres)
        self.data['num_pages'] = self.data['num_pages'].apply(self._parse_pages)

        self.data = self.data.dropna(subset=['book_title', 'author', 'average_rating'])

        self.data['genres'] = self.data['genres'].apply(
            lambda x: x if isinstance(x, list) else []
        )

        median_pages = self.data['num_pages'].median()
        self.data.loc[:, 'num_pages'] = self.data['num_pages'].fillna(median_pages)
        self.data['num_pages'] = self.data['num_pages'].astype('float32')

        self.data['popularity_score'] = self._calculate_popularity()

        return self.data

    def _parse_genres(self, genre_str: str) -> List[str]:
        if pd.isna(genre_str) or not isinstance(genre_str, str):
            return []
        try:
            genres = ast.literal_eval(genre_str)
            return genres if isinstance(genres, list) else []
        except (ValueError, SyntaxError):
            return []

    def _parse_pages(self, pages_str: str) -> float:
        if pd.isna(pages_str) or not isinstance(pages_str, str):
            return np.nan
        try:
            pages_list = ast.literal_eval(pages_str)
            if isinstance(pages_list, list) and len(pages_list) > 0 and pages_list[0] is not None:
                return float(pages_list[0])
        except (ValueError, SyntaxError, TypeError):
            pass
        return np.nan

    def _calculate_popularity(self) -> pd.Series:
        max_ratings = self.data['num_ratings'].max()
        if max_ratings == 0:
            return pd.Series(0.0, index=self.data.index)
        
        normalized_ratings = self.data['num_ratings'] / max_ratings
        rating_factor = self.data['average_rating'] / 5.0
        
        popularity = normalized_ratings * 0.6 + rating_factor * 0.4
        return popularity.astype('float32')

    def get_memory_usage(self) -> Dict[str, Any]:
        if self.data is None:
            return {"error": "No data loaded"}

        memory_usage = self.data.memory_usage(deep=True)

        return {
            "total_memory_mb": memory_usage.sum() / 1024 ** 2,
            "per_column_mb": (memory_usage / 1024 ** 2).to_dict(),
            "shape": self.data.shape
        }

    def load_and_preprocess(self) -> pd.DataFrame:
        self.load_data()
        return self.preprocess_data()


if __name__ == "__main__":
    loader = BookDataLoader("goodreads_books_2024.csv")

    print("Loading data...")
    df = loader.load_and_preprocess()

    print("\n=== Data Info ===")
    print(f"Shape: {df.shape}")
    print(f"\nColumns: {df.columns.tolist()}")

    print("\n=== Memory Usage ===")
    memory_info = loader.get_memory_usage()
    print(f"Total Memory: {memory_info['total_memory_mb']:.2f} MB")

    print("\n=== Sample Data ===")
    print(df.head())

    print("\n=== Data Types ===")
    print(df.dtypes)
