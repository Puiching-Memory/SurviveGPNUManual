interface HealthResponse {
  status: 'healthy' | 'error' | 'loading'
  message?: string
}

// Cache the promise to avoid creating a new one on every render
let healthPromise: Promise<HealthResponse> | null = null

export function useHealthStatus(): Promise<HealthResponse> {
  if (!healthPromise) {
    healthPromise = fetchHealthStatus()
  }
  return healthPromise
}

async function fetchHealthStatus(): Promise<HealthResponse> {
  try {
    // Health endpoint doesn't require auth, but use apiFetch for consistency
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    const response = await fetch(`${apiUrl}/api/health`)
    if (!response.ok) return { status: 'error' }
    const data = await response.json()
    return data as HealthResponse
  } catch (error) {
    return { status: 'error', message: error instanceof Error ? error.message : 'Unknown error' }
  }
}
