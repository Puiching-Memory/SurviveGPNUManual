import { createContext, useContext, useReducer, ReactNode, useCallback, useEffect } from 'react'
import { AuthState, LoginCredentials, RegisterCredentials, AuthResult } from '@/types/auth'
import { apiFetch } from '@/lib/api'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Action types
export const AUTH_ACTIONS = {
  LOGIN_SUCCESS: 'LOGIN_SUCCESS',
  LOGOUT: 'LOGOUT',
  SET_LOADING: 'SET_LOADING',
} as const

type AuthAction =
  | { type: typeof AUTH_ACTIONS.LOGIN_SUCCESS; payload: { token: string; user?: any } }
  | { type: typeof AUTH_ACTIONS.LOGOUT }
  | { type: typeof AUTH_ACTIONS.SET_LOADING; payload: boolean }

const AuthStateContext = createContext<AuthState | null>(null)
const AuthDispatchContext = createContext<{
  login: (credentials: LoginCredentials) => Promise<AuthResult>
  register: (credentials: RegisterCredentials) => Promise<AuthResult>
  logout: () => void
} | null>(null)

const authReducer = (state: AuthState, action: AuthAction): AuthState => {
  switch (action.type) {
    case AUTH_ACTIONS.LOGIN_SUCCESS:
      return {
        ...state,
        isAuthenticated: true,
        token: action.payload.token,
        user: action.payload.user || null,
        isLoading: false,
      }
    case AUTH_ACTIONS.LOGOUT:
      return {
        ...state,
        isAuthenticated: false,
        token: null,
        user: null,
      }
    case AUTH_ACTIONS.SET_LOADING:
      return {
        ...state,
        isLoading: action.payload,
      }
    default:
      return state
  }
}

interface AuthProviderProps {
  children: ReactNode
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [state, dispatch] = useReducer(authReducer, {
    isAuthenticated: !!localStorage.getItem('token'),
    token: localStorage.getItem('token'),
    isLoading: false,
    user: null,
  })
  
  // Load user on mount
  useEffect(() => {
    const loadUser = async () => {
      const token = localStorage.getItem('token')
      if (token) {
        try {
          const response = await apiFetch(`${API_URL}/api/auth/me`)
          if (response.ok) {
            const user = await response.json()
            dispatch({
              type: AUTH_ACTIONS.LOGIN_SUCCESS,
              payload: { token, user },
            })
          } else if (response.status === 401) {
            // Token expired, clear it
            localStorage.removeItem('token')
            dispatch({ type: AUTH_ACTIONS.LOGOUT })
          }
        } catch (e) {
          // Ignore errors (401 is handled by apiFetch)
        }
      }
    }
    loadUser()
    
    // Listen for logout events from apiFetch
    const handleLogout = () => {
      dispatch({ type: AUTH_ACTIONS.LOGOUT })
    }
    window.addEventListener('auth:logout', handleLogout)
    
    return () => {
      window.removeEventListener('auth:logout', handleLogout)
    }
  }, [])

  const login = useCallback(async (credentials: LoginCredentials): Promise<AuthResult> => {
    dispatch({ type: AUTH_ACTIONS.SET_LOADING, payload: true })

    try {
      const response = await fetch(`${API_URL}/api/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(credentials),
      })

      const data = await response.json()

      if (!response.ok) {
        dispatch({ type: AUTH_ACTIONS.SET_LOADING, payload: false })
        return {
          success: false,
          error: data.detail || 'Login failed',
        }
      }

      localStorage.setItem('token', data.access_token)
      
      // Fetch user info
      const userResponse = await apiFetch(`${API_URL}/api/auth/me`, {
        headers: {
          Authorization: `Bearer ${data.access_token}`,
        },
      })
      
      let user = null
      if (userResponse.ok) {
        user = await userResponse.json()
      }
      
      dispatch({
        type: AUTH_ACTIONS.LOGIN_SUCCESS,
        payload: { token: data.access_token, user },
      })

      return { success: true, error: null }
    } catch (error) {
      dispatch({ type: AUTH_ACTIONS.SET_LOADING, payload: false })
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Login failed',
      }
    }
  }, [])

  const register = useCallback(
    async (credentials: RegisterCredentials): Promise<AuthResult> => {
      dispatch({ type: AUTH_ACTIONS.SET_LOADING, payload: true })

      try {
        const { confirmPassword, ...registerData } = credentials
        const response = await fetch(`${API_URL}/api/auth/register`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(registerData),
        })

        const data = await response.json()

        if (!response.ok) {
          dispatch({ type: AUTH_ACTIONS.SET_LOADING, payload: false })
          return {
            success: false,
            error: data.detail || 'Registration failed',
          }
        }

        // After successful registration, automatically log in
        return login({
          email: registerData.email,
          password: registerData.password,
        })
      } catch (error) {
        dispatch({ type: AUTH_ACTIONS.SET_LOADING, payload: false })
        return {
          success: false,
          error: error instanceof Error ? error.message : 'Registration failed',
        }
      }
    },
    [login]
  )

  const logout = useCallback(() => {
    localStorage.removeItem('token')
    dispatch({ type: AUTH_ACTIONS.LOGOUT })
  }, [])

  const value = {
    login,
    register,
    logout,
  }

  return (
    <AuthStateContext.Provider value={state}>
      <AuthDispatchContext.Provider value={value}>{children}</AuthDispatchContext.Provider>
    </AuthStateContext.Provider>
  )
}

export function useAuthState() {
  const context = useContext(AuthStateContext)
  if (!context) {
    throw new Error('useAuthState must be used within an AuthProvider')
  }
  return context
}

export function useAuthDispatch() {
  const context = useContext(AuthDispatchContext)
  if (!context) {
    throw new Error('useAuthDispatch must be used within an AuthProvider')
  }
  return context
}

export function useAuth() {
  return {
    ...useAuthState(),
    ...useAuthDispatch(),
  }
}
