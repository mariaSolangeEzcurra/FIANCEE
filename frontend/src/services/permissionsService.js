import { apiRequest } from './api.js'
// Los endpoints deben existir en Django antes de activar persistencia remota.
export const getPermissions=token=>apiRequest('/permisos/',{token})
export const updatePermissions=(payload,token)=>apiRequest('/permisos/',{token,method:'PUT',body:JSON.stringify(payload)})
