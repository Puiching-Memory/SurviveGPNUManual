// Theme types
export type Theme = 'light' | 'dark'

// Notification types
export type NotificationType = 'info' | 'success' | 'warning' | 'error'

export interface Notification {
  show: boolean
  message: string
  type: NotificationType
}

// App Context types
export interface AppState {
  theme: Theme
  notification: Notification
  userPreferences: Record<string, unknown>
}

// API Response types
export interface HealthCheckResponse {
  status: string
  version: string
  timestamp: string
}

export interface ApiError {
  detail: string
  status_code: number
}
