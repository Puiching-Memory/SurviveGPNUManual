import { useNavigate } from 'react-router-dom'
import { Suspense, cache } from 'react'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/input'
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/Card'
import { useToast } from '@/hooks/use-toast'
import { useAuth } from '@/context/AuthContext'
import { useLoadingState } from '@/hooks/useLoadingState'

function LoginFormContent() {
  const navigate = useNavigate()
  const { login } = useAuth()
  const { toast } = useToast()
  const { state, setLoading, setError } = useLoadingState('login-form')

  const onSubmit = cache(async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setLoading(true)
    setError(null)

    const formData = new FormData(event.currentTarget)
    const email = formData.get('email') as string
    const password = formData.get('password') as string

    const result = await login({ email, password })

    if (result.success) {
      toast({
        title: '欢迎回来！',
        description: '您已成功登录。',
      })
      navigate('/dashboard')
    } else {
      setError(result.error || '登录时发生错误')
      toast({
        variant: 'destructive',
        title: '错误',
        description: result.error || '登录时发生错误',
      })
    }

    setLoading(false)
  })

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>登录</CardTitle>
        <CardDescription>在下方输入您的邮箱以登录账户</CardDescription>
      </CardHeader>
      <form onSubmit={onSubmit}>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Input
              id="email"
              name="email"
              type="email"
              placeholder="邮箱地址"
              required
              disabled={state.isLoading}
              className="w-full"
            />
          </div>
          <div className="space-y-2">
            <Input
              id="password"
              name="password"
              type="password"
              placeholder="请输入密码"
              required
              disabled={state.isLoading}
              className="w-full"
            />
          </div>
          {state.error && <div className="text-sm text-destructive">{state.error}</div>}
        </CardContent>
        <CardFooter className="flex justify-between">
          <Button
            variant="outline"
            onClick={() => navigate('/register')}
            type="button"
            disabled={state.isLoading}
          >
            注册
          </Button>
          <Button type="submit" disabled={state.isLoading}>
            {state.isLoading ? '登录中...' : '登录'}
          </Button>
        </CardFooter>
      </form>
    </Card>
  )
}

export default function LoginForm() {
  return (
    <Suspense fallback={<div>加载中...</div>}>
      <LoginFormContent />
    </Suspense>
  )
}
