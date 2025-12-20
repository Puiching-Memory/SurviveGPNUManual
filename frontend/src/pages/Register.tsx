import { Link } from 'react-router-dom'
import RegisterForm from '../features/auth/RegisterForm'

export default function Register() {
  return (
    <div className="min-h-[80vh] flex flex-col items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="w-full max-w-md space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-bold tracking-tight text-foreground">
            创建新账户
          </h2>
          <p className="mt-2 text-center text-sm text-muted-foreground">
            已有账户？{' '}
            <Link to="/login" className="font-medium text-primary hover:text-primary/80">
              在此登录
            </Link>
          </p>
        </div>
        <RegisterForm />
      </div>
    </div>
  )
}
