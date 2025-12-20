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

function RegisterFormContent() {
  const navigate = useNavigate()
  const { register } = useAuth()
  const { toast } = useToast()
  const { state, setLoading, setError } = useLoadingState('register-form')

  const onSubmit = cache(async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setLoading(true)
    setError(null)

    const formData = new FormData(event.currentTarget)
    const email = formData.get('email') as string
    const username = formData.get('username') as string
    const password = formData.get('password') as string
    const confirmPassword = formData.get('confirmPassword') as string

    if (password !== confirmPassword) {
      setError('密码不匹配')
      setLoading(false)
      return
    }

    const result = await register({ email, username, password, confirmPassword })

    if (result.success) {
      toast({
        title: '注册成功！',
        description: '您的账户已创建。',
      })
      navigate('/dashboard')
    } else {
      setError(result.error || '注册时发生错误')
      toast({
        variant: 'destructive',
        title: '错误',
        description: result.error || '注册时发生错误',
      })
    }

    setLoading(false)
  })

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>注册</CardTitle>
        <CardDescription>创建新账户</CardDescription>
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
              id="username"
              name="username"
              type="text"
              placeholder="选择用户名"
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
          <div className="space-y-2">
            <Input
              id="confirmPassword"
              name="confirmPassword"
              type="password"
              placeholder="请确认密码"
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
            onClick={() => navigate('/login')}
            type="button"
            disabled={state.isLoading}
          >
            登录
          </Button>
          <Button type="submit" disabled={state.isLoading}>
            {state.isLoading ? '创建账户中...' : '注册'}
          </Button>
        </CardFooter>
      </form>
    </Card>
  )
}

export default function RegisterForm() {
  return (
    <Suspense fallback={<div>加载中...</div>}>
      <RegisterFormContent />
    </Suspense>
  )
}
