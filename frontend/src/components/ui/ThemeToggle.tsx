import { MoonIcon, SunIcon } from 'lucide-react'
import { Button } from './Button'
import { useAppState, useAppDispatch, setTheme } from '../../context/AppContext'
import { Theme } from '../../types'

export function ThemeToggle() {
  const { theme } = useAppState()
  const dispatch = useAppDispatch()

  const toggleTheme = (): void => {
    const newTheme: Theme = theme === 'light' ? 'dark' : 'light'
    setTheme(dispatch, newTheme)
  }

  return (
    <Button
      onClick={toggleTheme}
      variant="ghost"
      aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} theme`}
    >
      {theme === 'light' ? <SunIcon /> : <MoonIcon />}
    </Button>
  )
}
