import { AuthProvider } from '../auth/AuthContext.jsx'
import { RouterProvider } from './routes.jsx'
export function Providers({ children }) { return <AuthProvider><RouterProvider>{children}</RouterProvider></AuthProvider> }
