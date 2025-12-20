import { Suspense } from 'react'
import { useNavigate } from 'react-router-dom'
import { CircleCheck, Sparkles } from 'lucide-react'
import { ErrorBoundary } from '../features/health/ErrorBoundary'
import { HealthStatus } from '../features/health/HealthStatus'
import { LoadingStatus } from '../features/health/LoadingStatus'
import { Button } from '../components/ui/Button'

type FeatureItem = {
  id: string
  text: string
}

const features: FeatureItem[] = [
  { id: '1', text: 'FastAPI 后端与健康检查' },
  { id: '2', text: 'React 19 现代模式' },
  { id: '3', text: '原生 Fetch API 集成' },
  { id: '4', text: '现代数据获取' },
  { id: '5', text: 'Tailwind CSS 深色模式' },
  { id: '6', text: '响应式设计' },
  { id: '7', text: '错误边界' },
  { id: '8', text: 'Docker 支持' },
]

export default function Home() {
  const navigate = useNavigate()

  return (
    <div className="space-y-12 py-8">
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-4 text-foreground">
          欢迎使用在线文档系统
        </h1>
        <p className="text-lg text-muted-foreground">
          基于 React 19 和 FastAPI 的现代化全栈文档管理平台
        </p>
      </div>

      <div className="grid gap-6">
        <div
          className="p-6 rounded-lg border border-border
          bg-card text-card-foreground shadow-sm hover:shadow-md transition-all"
        >
          <div className="flex items-start space-x-4">
            <div className="flex-shrink-0 p-2 rounded-lg bg-accent text-accent-foreground">
              <CircleCheck />
            </div>
            <div className="flex-1">
              <h2 className="text-xl font-semibold mb-4 text-card-foreground">后端状态</h2>
              <ErrorBoundary>
                <Suspense fallback={<LoadingStatus />}>
                  <HealthStatus />
                </Suspense>
              </ErrorBoundary>
            </div>
          </div>
        </div>

        <div
          className="p-6 rounded-lg border border-border
          bg-card text-card-foreground shadow-sm hover:shadow-md transition-all"
        >
          <div className="flex items-start space-x-4">
            <div className="flex-shrink-0 p-2 rounded-lg bg-accent text-accent-foreground">
              <Sparkles />
            </div>
            <div className="flex-1">
              <h2 className="text-xl font-semibold mb-4 text-card-foreground">功能特性</h2>
              <ul className="space-y-3 text-muted-foreground">
                {features.map(({ id, text }) => (
                  <li key={id} className="flex items-center">
                    <span className="text-primary mr-2">✓</span>
                    {text}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </div>

      <div className="flex justify-center space-x-4">
        <Button onClick={() => navigate('/dashboard')} variant="secondary">
          查看仪表板
        </Button>
      </div>
    </div>
  )
}
