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
  { id: '1', text: '主题化文档组织（指南/职业/博客）' },
  { id: '2', text: '文件系统文档管理' },
  { id: '3', text: '文档内容搜索与浏览' },
  { id: '4', text: '基于角色的访问控制' },
  { id: '5', text: 'JWT 身份验证' },
  { id: '6', text: '响应式设计，支持移动端' },
  { id: '7', text: '深色模式支持' },
  { id: '8', text: '现代化 UI 组件' },
]

export default function Home() {
  const navigate = useNavigate()

  return (
    <div className="space-y-12 py-8">
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-4 text-foreground">
          广师大生存手册
        </h1>
        <p className="text-lg text-muted-foreground">
          Survive GPNU Manual - 为广师大学子提供全方位的校园生活指南
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
        <Button onClick={() => navigate('/docs')} variant="secondary">
          浏览文档
        </Button>
        <Button onClick={() => navigate('/dashboard')} variant="default">
          进入仪表板
        </Button>
      </div>
    </div>
  )
}
