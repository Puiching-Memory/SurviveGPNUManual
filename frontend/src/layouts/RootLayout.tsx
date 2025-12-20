import { Link, Outlet, useNavigate, useLocation } from 'react-router-dom'
import { AppProvider } from '../context/AppContext'
import { Notification } from '../components/ui/Notification'
import { ThemeToggle } from '../components/ui/ThemeToggle'
import { useAuth } from '../context/AuthContext'
import { Button } from '../components/ui/Button'

const publicNavLinks = [
  { to: '/', label: '文档' },
] as const

const privateNavLinks = [
  { to: '/dashboard', label: '仪表板' },
] as const

const adminNavLinks = [
  { to: '/admin/packages', label: '文档包管理' },
] as const

function Navigation() {
  const navigate = useNavigate()
  const location = useLocation()
  const { isAuthenticated, logout, user } = useAuth()
  const linkBase =
    'text-card-foreground hover:text-primary hover:bg-accent/20 px-3 py-2 rounded-md text-sm font-medium transition-colors'
  const activeLink = 'text-primary font-semibold underline underline-offset-4'

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <nav className="bg-card text-card-foreground shadow-sm transition-colors">
      <div className="container mx-auto px-6">
        <div className="flex justify-between h-16 items-center">
          <div className="flex space-x-8">
            {publicNavLinks.map(({ to, label }) => (
              <Link
                key={to}
                to={to}
                className={location.pathname === to ? `${linkBase} ${activeLink}` : linkBase}
              >
                {label}
              </Link>
            ))}
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
            {isAuthenticated && user && (user.role === 'admin' || user.is_superuser) &&
              adminNavLinks.map(({ to, label }) => (
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
              {currentYear} 在线文档系统. 保留所有权利.
            </p>
          </div>
        </footer>
        <Notification />
      </div>
    </AppProvider>
  )
}
