import { use } from 'react'
import { StatusDot } from '../../components/ui/StatusDot'
import { useHealthStatus } from '../../hooks/useHealthStatus'

export function HealthStatus() {
  const data = use(useHealthStatus())

  return (
    <div className="flex items-center">
      <StatusDot status={data.status} />
      <span className="text-gray-600">状态: {data.status}</span>
    </div>
  )
}
