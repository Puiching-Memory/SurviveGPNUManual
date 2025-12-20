import { StatusDot } from '../../components/ui/StatusDot'

export function ErrorBoundary({ children }) {
  let error = undefined
  try {
    return children
  } catch (e) {
    error = e
  }

  return (
    <div className="flex items-center">
      <StatusDot status="error" />
      <span className="text-red-600">Error: {error?.message || 'Something went wrong'}</span>
    </div>
  )
}
