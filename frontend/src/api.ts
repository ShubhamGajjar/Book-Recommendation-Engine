import type { Book, Stats, RecommendationRequest, RecommendationResponse, SearchResponse, PopularResponse } from './types'

const API_BASE = '/api'

export const api = {
  async getStats(): Promise<Stats> {
    const response = await fetch(`${API_BASE}/stats`)
    if (!response.ok) {
      throw new Error('Failed to fetch stats')
    }
    return response.json()
  },

  async searchBooks(query: string, limit: number = 10): Promise<Book[]> {
    const response = await fetch(`${API_BASE}/search?q=${encodeURIComponent(query)}&limit=${limit}`)
    if (!response.ok) {
      throw new Error('Failed to search books')
    }
    const data: SearchResponse = await response.json()
    return data.books
  },

  async getPopularBooks(limit: number = 5): Promise<Book[]> {
    const response = await fetch(`${API_BASE}/popular?limit=${limit}`)
    if (!response.ok) {
      throw new Error('Failed to fetch popular books')
    }
    const data: PopularResponse = await response.json()
    return data.books
  },

  async getRecommendations(request: RecommendationRequest): Promise<Book[]> {
    const response = await fetch(`${API_BASE}/recommendations`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    })
    
    if (!response.ok) {
      const error = await response.json().catch(() => ({ error: 'Failed to get recommendations' }))
      throw new Error(error.error || 'Failed to get recommendations')
    }
    
    const data: RecommendationResponse = await response.json()
    return data.recommendations
  },
}

