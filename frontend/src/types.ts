export interface Book {
  id: number
  title: string
  author: string
  rating: number
  num_ratings: number
  genres: string[]
  score?: number
  popularity_score?: number
}

export interface Stats {
  total_books: number
  memory_mb: number
  average_rating: number
  total_ratings: number
  unique_authors: number
  avg_pages: number
}

export interface RecommendationRequest {
  book_title: string
  strategy: 'hybrid' | 'content' | 'popularity'
  n: number
}

export interface RecommendationResponse {
  recommendations: Book[]
}

export interface SearchResponse {
  books: Book[]
}

export interface PopularResponse {
  books: Book[]
}

