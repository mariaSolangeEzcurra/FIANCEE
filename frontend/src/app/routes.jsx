import {
  createContext,
  useContext,
  useEffect,
  useMemo,
  useState,
} from 'react'

const RouterContext = createContext(null)

export function RouterProvider({ children }) {
  const [path, setPath] = useState(
    () => window.location.pathname || '/',
  )

  useEffect(() => {
    const onPop = () => {
      setPath(window.location.pathname || '/')
    }

    window.addEventListener('popstate', onPop)

    return () => {
      window.removeEventListener('popstate', onPop)
    }
  }, [])

  const router = useMemo(
    () => ({
      path,
      navigate(to) {
        if (!to) return

        window.history.pushState({}, '', to)
        setPath(to)
        window.scrollTo({ top: 0, behavior: 'auto' })
      },
    }),
    [path],
  )

  return (
    <RouterContext.Provider value={router}>
      {children}
    </RouterContext.Provider>
  )
}

export function useRouter() {
  const value = useContext(RouterContext)

  if (!value) {
    throw new Error(
      'useRouter debe usarse dentro de RouterProvider',
    )
  }

  return value
}

export function AppLink({
  to,
  children,
  className,
  onClick,
  ...props
}) {
  const { navigate } = useRouter()

  return (
    <a
      href={to}
      className={className}
      onClick={event => {
        if (
          event.button !== 0 ||
          event.metaKey ||
          event.ctrlKey ||
          event.shiftKey ||
          event.altKey
        ) {
          return
        }

        event.preventDefault()
        onClick?.(event)
        navigate(to)
      }}
      {...props}
    >
      {children}
    </a>
  )
}