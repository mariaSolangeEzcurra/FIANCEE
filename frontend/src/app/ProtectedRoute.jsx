import { useAuth } from '../auth/AuthContext.jsx'
import { canAccessPath, homeForRole } from '../navigation/permissions.js'
export default function ProtectedRoute({ children, path }) {
 const { session } = useAuth()
 if (!session) return null
 if (!canAccessPath(session.roles || session.role, path)) return <section className="denied"><span className="eyebrow">ACCESO RESTRINGIDO</span><h1>No tienes permiso para ver esta interfaz</h1><p>Si necesitas acceso, solicita autorización a la persona administradora.</p><a className="button button-primary" href={homeForRole(session.roles || session.role)}>Volver al inicio</a></section>
 return children
}
