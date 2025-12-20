import { use, cache } from 'react'

interface LoadingState {
  isLoading: boolean
  error: string | null
}

// Create a global store for loading states
const loadingStates = new Map<string, LoadingState>()

// Initialize a loading state if it doesn't exist
const getOrCreateLoadingState = cache((id: string): LoadingState => {
  if (!loadingStates.has(id)) {
    loadingStates.set(id, {
      isLoading: false,
      error: null,
    })
  }
  return loadingStates.get(id)!
})

// Create a signal for each loading state
const loadingSignals = new Map<string, Promise<LoadingState>>()

const getLoadingSignal = cache((id: string): Promise<LoadingState> => {
  if (!loadingSignals.has(id)) {
    loadingSignals.set(id, Promise.resolve(getOrCreateLoadingState(id)))
  }
  return loadingSignals.get(id)!
})

export function useLoadingState(id: string) {
  const state = use(getLoadingSignal(id))

  const setLoading = cache((isLoading: boolean) => {
    const currentState = getOrCreateLoadingState(id)
    const newState = { ...currentState, isLoading }
    loadingStates.set(id, newState)
    loadingSignals.set(id, Promise.resolve(newState))
  })

  const setError = cache((error: string | null) => {
    const currentState = getOrCreateLoadingState(id)
    const newState = { ...currentState, error }
    loadingStates.set(id, newState)
    loadingSignals.set(id, Promise.resolve(newState))
  })

  return { state, setLoading, setError }
}
