// Cache the promise to avoid creating a new one on every render
let healthPromise = null

export function useHealthStatus() {
  if (!healthPromise) {
    healthPromise = fetchHealthStatus()
  }
  return healthPromise
}

async function fetchHealthStatus() {
  try {
    // Health endpoint doesn't require auth, but use apiFetch for consistency
    const response = await fetch(`${import.meta.env.VITE_API_URL}/api/health`)
    if (!response.ok) return { status: 'error' }
    const data = await response.json()
    return data
  } catch (error) {
    return { status: 'error', message: error instanceof Error ? error.message : 'Unknown error' }
  }
}
