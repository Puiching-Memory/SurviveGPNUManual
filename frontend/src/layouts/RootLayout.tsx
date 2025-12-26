import { Link, Outlet, useNavigate, useLocation } from 'react-router-dom'
import { AppProvider } from '../context/AppContext'
import { Notification } from '../components/ui/Notification'
import { ThemeToggle } from '../components/ui/ThemeToggle'
import { useAuth } from '../context/AuthContext'
import { Button } from '../components/ui/Button'

const publicNavLinks = [
  { to: '/docs', label: '文档' },
] as const

const documentCategories = [
  { to: '/docs?category=guides', label: '核心指南', category: 'guides' },
  { to: '/docs?category=career', label: '职业升学', category: 'career' },
  { to: '/docs?category=blog', label: '博客文章', category: 'blog' },
] as const

const privateNavLinks = [
  { to: '/dashboard', label: '仪表板' },
] as const

function Navigation() {
  const navigate = useNavigate()
  const location = useLocation()
  const { isAuthenticated, logout } = useAuth()
  const linkBase =
    'text-card-foreground hover:text-primary hover:bg-accent/20 px-3 py-2 rounded-md text-sm font-medium transition-colors'
  const activeLink = 'text-primary font-semibold underline underline-offset-4'

  // 检查当前路径是否匹配某个分类
  const getActiveCategory = () => {
    const searchParams = new URLSearchParams(location.search)
    const category = searchParams.get('category')
    if (category) {
      return category
    }
    // 如果路径包含分类信息，也可以从路径中提取
    if (location.pathname.startsWith('/docs/')) {
      // 可以根据文档路径推断分类，这里简化处理
      return null
    }
    return null
  }

  const activeCategory = getActiveCategory()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <nav className="bg-card text-card-foreground shadow-sm transition-colors">
      <div className="container mx-auto px-6">
        <div className="flex justify-between h-16 items-center">
          <div className="flex space-x-6 items-center">
            {publicNavLinks.map(({ to, label }) => (
              <Link
                key={to}
                to={to}
                className={location.pathname === to ? `${linkBase} ${activeLink}` : linkBase}
              >
                {label}
              </Link>
            ))}
            {/* 文档分类分区 */}
            {location.pathname === '/docs' && (
              <div className="flex items-center space-x-1 border-l border-border pl-6 ml-2">
                <span className="text-xs text-muted-foreground mr-2 font-medium">文档分类：</span>
                {documentCategories.map(({ to, label, category }) => (
                  <Link
                    key={category}
                    to={to}
                    className={
                      activeCategory === category
                        ? `${linkBase} ${activeLink}`
                        : linkBase
                    }
                  >
                    {label}
                  </Link>
                ))}
              </div>
            )}
            {isAuthenticated &&
              privateNavLinks.map(({ to, label }) => (
                <Link
                  key={to}
                  to={to}
                  className={location.pathname === to ? `${linkBase} ${activeLink}` : linkBase}
                >
                  {label}
                </Link>
              ))}
          </div>
          <div className="flex items-center space-x-4">
            <ThemeToggle />
            {isAuthenticated ? (
              <Button
                variant="ghost"
                onClick={handleLogout}
                className="text-card-foreground hover:text-primary hover:bg-accent/20"
              >
                退出登录
              </Button>
            ) : (
              <Link
                to="/login"
                className={location.pathname === '/login' ? `${linkBase} ${activeLink}` : linkBase}
              >
                登录
              </Link>
            )}
          </div>
        </div>
      </div>
    </nav>
  )
}

export default function RootLayout() {
  const currentYear = new Date().getFullYear()

  return (
    <AppProvider>
      <div className="min-h-screen flex flex-col bg-background text-foreground transition-colors">
        <Navigation />
        <main className="flex-1 container mx-auto px-6 py-8">
          <Outlet />
        </main>
        <footer className="bg-card text-card-foreground shadow-sm transition-colors mt-auto">
          <div className="container mx-auto px-6 py-4">
            <p className="text-center text-muted-foreground">
              © {currentYear} 广师大生存手册. 保留所有权利.
            </p>
          </div>
        </footer>
        <Notification />
      </div>
    </AppProvider>
  )
}
