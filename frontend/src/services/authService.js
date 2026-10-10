import { apiRequest } from './api.js'

// El usuario no elige perfil: Django devuelve los roles asignados a su cuenta.
export const loginRequest = (username, password) => apiRequest('/auth/login/', {
  method: 'POST',
  body: JSON.stringify({ username, password }),
})

export const logoutRequest = token => apiRequest('/auth/logout/', { method: 'POST', token })
export const currentUserRequest = token => apiRequest('/auth/me/', { method: 'GET', token })
