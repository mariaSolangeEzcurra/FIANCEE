import { createContext, useCallback, useContext, useMemo, useState } from 'react'
import { clearSession, normalizeRole, readSession, saveSession } from './session.js'

const AuthContext = createContext(null)
const API_URL = (import.meta.env.VITE_API_URL || '/api').replace(/\/$/, '')

export function AuthProvider({ children }) {
  const [session, setSession] = useState(readSession)

  const login = useCallback(async (username, password) => {
    let response
    try {
      response = await fetch(`${API_URL}/auth/login/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({ username: username.trim(), password }),
      })
    } catch {
      throw new Error('No se pudo conectar con el servidor. Comprueba que Docker y el backend estén activos.')
    }

    const data = await response.json().catch(() => ({}))
    if (!response.ok) {
      throw new Error(data?.detail || `No se pudo iniciar sesión (HTTP ${response.status}).`)
    }
    if (!data.token) throw new Error('El servidor no devolvió el token de acceso.')

    const assignedRoles = (Array.isArray(data.roles) ? data.roles : [data.rol || data.role])
      .filter(Boolean).map(normalizeRole)
    if (!assignedRoles.length) {
      throw new Error('Tu cuenta no tiene un área asignada. Solicita que Gerencia o el superadministrador te asigne un rol.')
    }

    const next = {
      token: data.token,
      username: data.username || username.trim(),
      roles: [...new Set(assignedRoles)],
      role: assignedRoles[0],
      isSuperuser: Boolean(data.es_superusuario),
      fullName: data.nombre || data.full_name || data.username || username.trim(),
    }
    saveSession(next)
    setSession(next)
    return next
  }, [])

  const logout = useCallback(async () => {
    try {
      if (session?.token) {
        await fetch(`${API_URL}/auth/logout/`, {
          method: 'POST',
          headers: { Authorization: `Token ${session.token}` },
        })
      }
    } catch {
      // La sesión local se elimina incluso si el servidor no responde.
    }
    clearSession()
    setSession(null)
  }, [session])

  const value = useMemo(() => ({ session, login, logout }), [session, login, logout])
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const value = useContext(AuthContext)
  if (!value) throw new Error('useAuth debe usarse dentro de AuthProvider')
  return value
}
