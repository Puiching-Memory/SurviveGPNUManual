import { createContext, useContext, useReducer, ReactNode, Dispatch } from 'react'
import { AppState, Theme, NotificationType } from '../types'
import { AuthProvider } from './AuthContext'

// Action types
export const ACTIONS = {
  SET_THEME: 'SET_THEME',
  SET_USER_PREFERENCES: 'SET_USER_PREFERENCES',
  UPDATE_NOTIFICATION: 'UPDATE_NOTIFICATION',
} as const

interface SetThemeAction {
  type: typeof ACTIONS.SET_THEME
  payload: Theme
}

interface SetUserPreferencesAction {
  type: typeof ACTIONS.SET_USER_PREFERENCES
  payload: Record<string, unknown>
}

interface UpdateNotificationAction {
  type: typeof ACTIONS.UPDATE_NOTIFICATION
  payload: {
    message?: string
    type?: NotificationType
    show?: boolean
  }
}

type Action = SetThemeAction | SetUserPreferencesAction | UpdateNotificationAction

// Get initial theme from localStorage or system preference
const getInitialTheme = (): Theme => {
  if (typeof window !== 'undefined') {
    const savedTheme = localStorage.getItem('theme') as Theme | null
    if (savedTheme && (savedTheme === 'light' || savedTheme === 'dark')) {
      return savedTheme
    }
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
  }
  return 'light'
}

// Initial state
const initialState: AppState = {
  theme: getInitialTheme(),
  userPreferences: {},
  notification: {
    message: '',
    type: 'info',
    show: false,
  },
}

// Reducer
function appReducer(state: AppState, action: Action): AppState {
  switch (action.type) {
    case ACTIONS.SET_THEME: {
      const newTheme = action.payload
      localStorage.setItem('theme', newTheme)
      // Update DOM synchronously with state change
      const root = window.document.documentElement
      root.classList.remove('light', 'dark')
      root.classList.add(newTheme)
      return {
        ...state,
        theme: newTheme,
      }
    }
    case ACTIONS.SET_USER_PREFERENCES:
      return {
        ...state,
        userPreferences: {
          ...state.userPreferences,
          ...action.payload,
        },
      }
    case ACTIONS.UPDATE_NOTIFICATION:
      return {
        ...state,
        notification: {
          ...state.notification,
          ...action.payload,
        },
      }
    default:
      throw new Error(`Unknown actionS`)
  }
}

interface AppProviderProps {
  children: ReactNode
}

export function AppProvider({ children }: AppProviderProps) {
  const [state, dispatch] = useReducer(appReducer, initialState)

  // Initialize theme class on mount
  if (typeof window !== 'undefined') {
    const root = window.document.documentElement
    root.classList.remove('light', 'dark')
    root.classList.add(state.theme)
  }

  return (
    <AppContext.Provider value={state}>
      <AppDispatchContext.Provider value={dispatch}>
        <AuthProvider>{children}</AuthProvider>
      </AppDispatchContext.Provider>
    </AppContext.Provider>
  )
}

// Custom hooks for using the context
export function useAppState(): AppState {
  const context = useContext(AppContext)
  if (context === null) {
    throw new Error('useAppState must be used within an AppProvider')
  }
  return context
}

export function useAppDispatch(): Dispatch<Action> {
  const context = useContext(AppDispatchContext)
  if (context === null) {
    throw new Error('useAppDispatch must be used within an AppProvider')
  }
  return context
}

// Action creators
export function showNotification(
  dispatch: Dispatch<Action>,
  message: string,
  type: NotificationType = 'info'
): void {
  dispatch({
    type: ACTIONS.UPDATE_NOTIFICATION,
    payload: {
      message,
      type,
      show: true,
    },
  })

  // Auto-hide notification after 5 seconds
  setTimeout(() => {
    dispatch({
      type: ACTIONS.UPDATE_NOTIFICATION,
      payload: {
        show: false,
      },
    })
  }, 5000)
}

export function setTheme(dispatch: Dispatch<Action>, theme: Theme): void {
  dispatch({
    type: ACTIONS.SET_THEME,
    payload: theme,
  })
}

export function setUserPreferences(
  dispatch: Dispatch<Action>,
  preferences: Record<string, unknown>
): void {
  dispatch({
    type: ACTIONS.SET_USER_PREFERENCES,
    payload: preferences,
  })
}

const AppContext = createContext<AppState | null>(null)
const AppDispatchContext = createContext<Dispatch<Action> | null>(null)
