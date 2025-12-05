import time
import pandas as pd
from data_loader import BookDataLoader
from book_recommender import BookRecommendationEngine


def print_section(title: str):
    print("\n" + "=" * 80)
    print(f" {title}")
    print("=" * 80)


def demonstrate_data_loading():
    print_section("PART 1: EFFICIENT DATA LOADING")

    print("\n📥 Loading data with optimized columns and dtypes...")
    start_time = time.time()

    loader = BookDataLoader("goodreads_books_2024.csv")
    books_df = loader.load_and_preprocess()

    load_time = time.time() - start_time

    print(f"✅ Data loaded in {load_time:.2f} seconds")
    print(f"📊 Dataset shape: {books_df.shape}")

    print("\n💾 Memory Usage Analysis:")
    memory_info = loader.get_memory_usage()
    print(f"Total memory: {memory_info['total_memory_mb']:.2f} MB")

    print("\nMemory per column:")
    for col, mem in memory_info['per_column_mb'].items():
        if isinstance(mem, float):
            print(f"  {col:20s}: {mem:.2f} MB")

    print("\n📋 Optimized Data Types:")
    print(books_df.dtypes)

    print("\n👀 Sample Data (first 3 rows):")
    print(books_df.head(3)[['book_title', 'author', 'average_rating', 'num_ratings']])

    return books_df, loader


def demonstrate_content_based(engine: BookRecommendationEngine):
    print_section("PART 2: CONTENT-BASED RECOMMENDATIONS")

    test_books = [
        "Harry Potter and the Half-Blood Prince",
        "1984",
        "The Great Gatsby"
    ]

    for book_title in test_books:
        print(f"\n🔍 Finding books similar to: '{book_title}'")
        print("-" * 80)

        start_time = time.time()
        recommendations = engine.get_recommendations(
            book_title,
            strategy='content',
            n=5
        )
        elapsed = time.time() - start_time

        if recommendations:
            engine.display_recommendations(recommendations)
            print(f"\n⏱️  Recommendation time: {elapsed:.4f} seconds")
        else:
            print(f"❌ Book not found in dataset")


def demonstrate_popularity(engine: BookRecommendationEngine):
    print_section("PART 3: POPULARITY-BASED RECOMMENDATIONS")

    print("\n📈 Top 5 Most Popular Books Overall:")
    print("-" * 80)

    popular_books = engine.books_df.nlargest(5, 'popularity_score')

    for i, (_, book) in enumerate(popular_books.iterrows(), 1):
        genres_display = ', '.join(book['genres'][:3]) if book['genres'] else 'N/A'
        print(f"\n{i}. {book['book_title']}")
        print(f"   Author: {book['author']}")
        print(f"   Rating: {book['average_rating']:.2f} ⭐")
        print(f"   Ratings: {book['num_ratings']:,}")
        print(f"   Genres: {genres_display}")
        print(f"   Popularity Score: {book['popularity_score']:.4f}")


def demonstrate_hybrid(engine: BookRecommendationEngine):
    print_section("PART 4: HYBRID RECOMMENDATIONS")

    test_book = "Harry Potter and the Half-Blood Prince"

    print(f"\n🎯 Hybrid recommendations for: '{test_book}'")
    print("(Combining content similarity + popularity)")
    print("-" * 80)

    start_time = time.time()
    recommendations = engine.get_recommendations(
        test_book,
        strategy='hybrid',
        n=5
    )
    elapsed = time.time() - start_time

    if recommendations:
        engine.display_recommendations(recommendations)
        print(f"\n⏱️  Recommendation time: {elapsed:.4f} seconds")
    else:
        print("❌ Book not found in dataset")


def compare_strategies(engine: BookRecommendationEngine):
    print_section("PART 5: STRATEGY COMPARISON")

    test_book = "The Hunger Games"

    print(f"\n📊 Comparing recommendation strategies for: '{test_book}'")
    print("=" * 80)

    strategies = ['content', 'hybrid']
    results = {}

    for strategy in strategies:
        print(f"\n🔸 Strategy: {strategy.upper()}")
        print("-" * 80)

        start_time = time.time()
        recommendations = engine.get_recommendations(test_book, strategy=strategy, n=5)
        elapsed = time.time() - start_time

        results[strategy] = recommendations

        if recommendations:
            for i, (book_id, title, score) in enumerate(recommendations, 1):
                print(f"{i}. {title[:60]:60s} | Score: {score:.3f}")
            print(f"\n⏱️  Time: {elapsed:.4f}s")
        else:
            print("❌ No recommendations found")

    print("\n📝 Analysis:")
    print("-" * 80)
    print("Content-based focuses on similar features (genres, author, etc.)")
    print("Hybrid balances similarity with overall popularity")
    print("\nNotice how the recommendations and scores differ between strategies!")


def performance_analysis(engine: BookRecommendationEngine):
    print_section("PART 6: PERFORMANCE ANALYSIS")

    print("\n⚡ Timing Analysis:")
    print("-" * 80)

    test_books = [
        "Harry Potter",
        "1984",
        "The Hobbit"
    ]

    times = []

    for book in test_books:
        start = time.time()
        recommendations = engine.get_recommendations(book, strategy='content', n=10)
        elapsed = time.time() - start
        times.append(elapsed)

        print(f"Recommendations for '{book:30s}': {elapsed:.4f}s")

    avg_time = sum(times) / len(times)
    print(f"\n📊 Average recommendation time: {avg_time:.4f}s")

    print("\n💡 Performance Notes:")
    print("- Similarity matrix is pre-computed (one-time cost)")
    print("- Each recommendation query is fast (just lookups and sorts)")
    print("- For larger datasets, consider on-demand similarity computation")


def memory_comparison(loader: BookDataLoader):
    print_section("MEMORY OPTIMIZATION COMPARISON")

    print("\n📊 Comparing memory usage with and without optimization...")
    print("-" * 80)

    optimized_memory = loader.get_memory_usage()
    
    print(f"\nWith optimization:")
    print(f"  Total memory: {optimized_memory['total_memory_mb']:.2f} MB")
    print(f"  Number of books: {optimized_memory['shape'][0]:,}")
    print(f"  Memory per book: {optimized_memory['total_memory_mb'] / optimized_memory['shape'][0] * 1024:.2f} KB")


def main():
    print("\n" + "🎬" * 40)
    print("  BOOK RECOMMENDATION ENGINE DEMONSTRATION")
    print("  CS 5130 - Lab 6")
    print("🎬" * 40)

    books_df, loader = demonstrate_data_loading()

    print_section("BUILDING RECOMMENDATION ENGINE")
    print("\n🔧 Initializing recommendation engine...")
    print("   (This may take a moment while computing similarity matrix...)")

    start_time = time.time()
    engine = BookRecommendationEngine(books_df)
    build_time = time.time() - start_time

    print(f"✅ Engine ready! (built in {build_time:.2f} seconds)")

    demonstrate_content_based(engine)
    demonstrate_popularity(engine)
    demonstrate_hybrid(engine)
    compare_strategies(engine)
    performance_analysis(engine)
    memory_comparison(loader)

    print_section("DEMONSTRATION COMPLETE")
    print("\n✨ All recommendation strategies demonstrated successfully!")
    print("\n💡 Key Takeaways:")
    print("   1. Efficient data loading saves significant memory")
    print("   2. Different strategies have different strengths")
    print("   3. Vectorized operations enable fast recommendations")
    print("   4. Good software design makes the system extensible")

    print("\n" + "=" * 80)
    print("Thank you for using the Book Recommendation Engine! 📚")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()

