import { Link } from 'react-router-dom'
import LoginForm from '../features/auth/LoginForm'

export default function Login() {
  return (
    <div className="min-h-[80vh] flex flex-col items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="w-full max-w-md space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-bold tracking-tight text-foreground">
            登录您的账户
          </h2>
          <p className="mt-2 text-center text-sm text-muted-foreground">
            或{' '}
            <Link to="/register" className="font-medium text-primary hover:text-primary/80">
              创建新账户
            </Link>
          </p>
        </div>
        <LoginForm />
      </div>
    </div>
  )
}
