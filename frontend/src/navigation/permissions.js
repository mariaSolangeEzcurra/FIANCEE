import { getAllNavigation, homeForRole as configuredHome } from './navigationConfig.js'
export function canAccessPath(roleOrRoles, path) {
 const roles = Array.isArray(roleOrRoles) ? roleOrRoles : [roleOrRoles]
 const page = getAllNavigation().find(item => item.path === path && item.enabled !== false)
 return Boolean(page && page.roles.some(role => roles.includes(role)))
}
export function canPerform(roleOrRoles, path, action) {
 const roles = Array.isArray(roleOrRoles) ? roleOrRoles : [roleOrRoles]
 const page = getAllNavigation().find(item => item.path === path && item.enabled !== false)
 if (!page || !page.roles.some(role => roles.includes(role))) return false
 return roles.some(role => {
   const allowed = page.actions?.[role]
   return Array.isArray(allowed) ? allowed.includes(action) : action === 'view'
 })
}
export function homeForRole(roleOrRoles) {
 const roles = Array.isArray(roleOrRoles) ? roleOrRoles : [roleOrRoles]
 return configuredHome(roles)
}
