import { useAppState, useAppDispatch, ACTIONS } from '../../context/AppContext'
import { NotificationType } from '../../types'

const NOTIFICATION_COLORS: Record<NotificationType, string> = {
  info: 'bg-blue-500 dark:bg-blue-600',
  success: 'bg-green-500 dark:bg-green-600',
  error: 'bg-red-500 dark:bg-red-600',
  warning: 'bg-yellow-500 dark:bg-yellow-600',
}

export function Notification() {
  const { notification } = useAppState()
  const dispatch = useAppDispatch()

  if (!notification.show) return null

  const handleClose = () => {
    dispatch({
      type: ACTIONS.UPDATE_NOTIFICATION,
      payload: { show: false },
    })
  }

  const bgColor = NOTIFICATION_COLORS[notification.type]

  return (
    <div
      className={`fixed bottom-4 right-4 ${bgColor} text-white px-6 py-3 rounded-lg shadow-lg 
        flex items-center justify-between min-w-[300px] transition-all z-50`}
      role="alert"
    >
      <span>{notification.message}</span>
      <button
        onClick={handleClose}
        className="ml-4 text-white hover:text-gray-200 focus:outline-none transition-colors"
        aria-label="Close notification"
        type="button"
      >
        ✕
      </button>
    </div>
  )
}
