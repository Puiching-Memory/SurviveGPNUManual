import { ReactNode } from 'react'
import { Navigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

interface AdminRouteProps {
  children: ReactNode
}

export function AdminRoute({ children }: AdminRouteProps) {
  const { isAuthenticated, user } = useAuth()

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  if (!user || (user.role !== 'admin' && !user.is_superuser)) {
    return <Navigate to="/" replace />
  }

  return <>{children}</>
}

