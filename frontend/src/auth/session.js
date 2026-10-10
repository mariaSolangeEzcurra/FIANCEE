const KEY = 'fiancee_session'
export function readSession() {
  try {
    const value = JSON.parse(sessionStorage.getItem(KEY) || 'null')
    if (value && !Array.isArray(value.roles)) value.roles = value.role ? [value.role] : []
    return value
  } catch { return null }
}
export function saveSession(session) { sessionStorage.setItem(KEY, JSON.stringify(session)) }
export function clearSession() { sessionStorage.removeItem(KEY) }
export function normalizeRole(value) {
  const role = String(value || '').trim().toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '')
  if (role.includes('comercial')) return 'comercial'
  if (role.includes('jefa') || (role.includes('taller') && role.includes('jef'))) return 'jefa_taller'
  if (role === 'taller' || role.includes('trabajador') || role.includes('operario')) return 'taller'
  if (role.includes('gerencia') || role.includes('admin')) return 'gerencia'
  return role
}
