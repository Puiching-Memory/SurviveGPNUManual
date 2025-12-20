import { Suspense } from 'react'
import { ChartColumnIncreasing, Clock1, Zap } from 'lucide-react'
import { useAppDispatch } from '../context/AppContext'
import { showNotification } from '../context/AppContext'

export default function Dashboard() {
  const dispatch = useAppDispatch()

  const handleCardClick = (title: string) => {
    showNotification(dispatch, `Clicked ${title} card`, 'info')
  }

  return (
    <div className="space-y-8">
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-4 text-foreground">仪表板</h1>
        <p className="text-lg text-muted-foreground">
          监控您的应用指标和性能
        </p>
      </div>

      <Suspense
        fallback={
          <div className="text-center py-8 text-muted-foreground">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4" />
            加载仪表板数据中...
          </div>
        }
      >
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <DashboardCard
            title="统计信息"
            description="查看关键指标和分析"
            icon={<ChartColumnIncreasing />}
            onClick={handleCardClick}
          />
          <DashboardCard
            title="最近活动"
            description="跟踪最新更新和更改"
            icon={<Clock1 />}
            onClick={handleCardClick}
          />
          <DashboardCard
            title="性能"
            description="监控系统性能指标"
            icon={<Zap />}
            onClick={handleCardClick}
          />
        </div>
      </Suspense>
    </div>
  )
}

function DashboardCard({
  title,
  description,
  icon,
  onClick,
}: {
  title: string
  description: string
  icon: React.ReactNode
  onClick: (title: string) => void
}) {
  return (
    <div
      className="p-6 rounded-lg border border-border
        bg-card text-card-foreground shadow-sm hover:shadow-md transition-all
        cursor-pointer group"
      onClick={() => onClick(title)}
    >
      <div className="flex items-start space-x-4">
        <div
          className="flex-shrink-0 p-2 rounded-lg bg-accent text-accent-foreground
          group-hover:bg-accent/80 dark:group-hover:bg-accent/80 transition-colors"
        >
          {icon}
        </div>
        <div>
          <h2
            className="text-xl font-semibold mb-2 text-card-foreground group-hover:text-primary
            transition-colors"
          >
            {title}
          </h2>
          <p className="text-muted-foreground">{description}</p>
        </div>
      </div>
    </div>
  )
}
