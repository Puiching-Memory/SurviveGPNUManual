import { createBrowserRouter, redirect } from 'react-router-dom'
import { lazy, Suspense } from 'react'
import RootLayout from '../layouts/RootLayout'
import { ProtectedRoute } from '../components/ProtectedRoute'
import { AdminRoute } from '../components/AdminRoute'

// Lazy load components
const Dashboard = lazy(() => import('../pages/Dashboard'))
const Login = lazy(() => import('../pages/Login'))
const Register = lazy(() => import('../pages/Register'))
const Home = lazy(() => import('../pages/Home'))
const DocumentList = lazy(() => import('../pages/DocumentList'))
const DocumentView = lazy(() => import('../pages/DocumentView'))
const DocumentEdit = lazy(() => import('../pages/DocumentEdit'))

// Error boundary component
function ErrorBoundary() {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold text-red-600 mb-4">出错了！</h1>
      <p className="text-lg mb-4">发生了错误，请重试。</p>
      <a href="/" className="text-blue-600 hover:underline">
        返回首页
      </a>
    </div>
  )
}

// Loading component
function PageLoader() {
  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
    </div>
  )
}

const routes = {
  public: [
    {
      index: true,
      element: <Home />,
    },
    {
      path: 'docs',
      element: <DocumentList />,
    },
    {
      path: 'login',
      element: <Login />,
    },
    {
      path: 'register',
      element: <Register />,
    },
    {
      path: 'docs/:slug',
      element: <DocumentView />,
    },
  ],
  protected: [
    {
      path: 'dashboard',
      element: <Dashboard />,
    },
    {
      path: 'docs/:id/edit',
      element: <DocumentEdit />,
    },
  ],
}

const withSuspense = (element: React.ReactNode) => (
  <Suspense fallback={<PageLoader />}>{element}</Suspense>
)

const withProtection = (element: React.ReactNode) => (
  <ProtectedRoute>{withSuspense(element)}</ProtectedRoute>
)

const withAdminProtection = (element: React.ReactNode) => (
  <AdminRoute>{withSuspense(element)}</AdminRoute>
)

export const router = createBrowserRouter([
  {
    path: '/',
    element: <RootLayout />,
    errorElement: <ErrorBoundary />,
    children: [
      // Public routes
      ...routes.public.map((route) => ({
        ...route,
        element: withSuspense(route.element),
      })),

      // Protected routes
      ...routes.protected.map((route) => ({
        ...route,
        element:
          route.path === 'docs/:id/edit'
            ? withAdminProtection(route.element)
            : withProtection(route.element),
      })),

      // Catch-all route
      {
        path: '*',
        loader: () => redirect('/'),
      },
    ],
  },
])
