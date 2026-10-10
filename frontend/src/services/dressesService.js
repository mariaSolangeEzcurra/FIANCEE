import { apiRequest } from './api.js'
export const getDresses=token=>apiRequest('/vestidos/',{token})
export const getDress=(id,token)=>apiRequest(`/vestidos/${id}/`,{token})
