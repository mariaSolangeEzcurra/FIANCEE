import { apiRequest } from './api.js'
export const getProductionOrders=token=>apiRequest('/produccion/',{token})
export const getCapacity=token=>apiRequest('/produccion/capacidad/',{token})
