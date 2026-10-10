// En desarrollo, Vite reenvía /api al contenedor de Django.
const API_URL = (import.meta.env.VITE_API_URL || '/api').replace(/\/$/, '')

export async function apiRequest(path, { token, ...options } = {}) {
  let response
  try {
    response = await fetch(`${API_URL}${path.startsWith('/') ? path : `/${path}`}`, {
      ...options,
      headers: {
        Accept: 'application/json',
        ...(options.body ? { 'Content-Type': 'application/json' } : {}),
        ...(token ? { Authorization: `Token ${token}` } : {}),
        ...(options.headers || {}),
      },
    })
  } catch {
    throw new Error('No se pudo conectar con el servidor. Comprueba que Docker y el backend estén activos.')
  }
  const data = await response.json().catch(() => null)
  if (!response.ok) throw new Error(data?.detail || data?.message || `Error de solicitud (${response.status})`)
  return data
}
