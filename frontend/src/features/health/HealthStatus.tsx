import { use } from 'react'
import { StatusDot } from '../../components/ui/StatusDot'
import { useHealthStatus } from '../../hooks/useHealthStatus'

interface HealthData {
  status: 'healthy' | 'error' | 'loading'
  message?: string
}

export function HealthStatus() {
  const data = use(useHealthStatus()) as HealthData

  return (
    <div className="flex items-center">
      <StatusDot status={data.status || 'error'} />
      <span className="text-gray-600">状态: {data.status || 'unknown'}</span>
    </div>
  )
}
