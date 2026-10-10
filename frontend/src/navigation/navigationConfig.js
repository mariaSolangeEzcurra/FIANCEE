// Catálogo central de interfaces. Ajusta aquí nombres, rutas, orden e iconos.
export const ROLES = [
 { id: 'comercial', label: 'Comercial' }, { id: 'jefa_taller', label: 'Jefa de taller' }, { id: 'taller', label: 'Taller' }, { id: 'gerencia', label: 'Gerencia' },
]
export const NAVIGATION = [
 { id:'com-home', label:'Inicio', path:'/comercial', icon:'⌂', roles:['comercial'], group:'Principal', description:'Resumen de actividad comercial.' },
 { id:'com-sim', label:'Simulador de capacidad', path:'/comercial/simulador', icon:'◷', roles:['comercial','jefa_taller','gerencia'], group:'Comercial', description:'Evalúa la viabilidad de aceptar un nuevo vestido.' },
 { id:'com-contracts', label:'Contratos', path:'/comercial/contratos', icon:'▤', roles:['comercial','gerencia'], group:'Comercial', description:'Consulta y seguimiento de contratos.' },
 { id:'com-summary', label:'Resumen comercial', path:'/comercial/resumen', icon:'▥', roles:['comercial'], group:'Comercial', description:'Actividad y metas comerciales.' },
 { id:'tall-home', label:'Inicio', path:'/taller', icon:'⌂', roles:['jefa_taller'], group:'Principal', description:'Indicadores y pendientes del taller.' },
 { id:'tall-dresses', label:'Vestidos', path:'/taller/vestidos', icon:'♧', roles:['jefa_taller','gerencia'], group:'Producción', description:'Fichas, estado y seguimiento de vestidos.' },
 { id:'tall-queue', label:'Cola de producción', path:'/taller/cola', icon:'☷', roles:['jefa_taller','gerencia'], group:'Producción', description:'Prioridades y orden de los procesos.' },
 { id:'tall-capacity', label:'Capacidad', path:'/taller/capacidad', icon:'◴', roles:['jefa_taller','gerencia'], group:'Producción', description:'Carga, horas disponibles y cuellos de botella.' },
 { id:'tall-staff', label:'Personal', path:'/taller/personal', icon:'♙', roles:['jefa_taller','gerencia'], group:'Equipo', description:'Disponibilidad y asignaciones del equipo.' },
 { id:'tall-alerts', label:'Alertas', path:'/taller/alertas', icon:'⚑', roles:['jefa_taller','gerencia'], group:'Equipo', description:'Retrasos, bloqueos y riesgos operativos.' },
 { id:'worker-home', label:'Mi jornada', path:'/trabajador', icon:'⌂', roles:['taller'], group:'Mi trabajo', description:'Resumen de tareas y vestidos asignados.' },
 { id:'worker-hours', label:'Registrar horas', path:'/trabajador/registrar', icon:'◷', roles:['taller'], group:'Mi trabajo', description:'Registra el tiempo real dedicado a un proceso.' },
 { id:'worker-dresses', label:'Mis vestidos', path:'/trabajador/vestidos', icon:'♧', roles:['taller'], group:'Mi trabajo', description:'Vestidos asignados y su estado.' },
 { id:'worker-notes', label:'Mis observaciones', path:'/trabajador/observaciones', icon:'▤', roles:['taller'], group:'Mi trabajo', description:'Registra avances, incidencias o bloqueos.' },
 { id:'management-home', label:'Dashboard', path:'/gerencia', icon:'⌂', roles:['gerencia'], group:'Principal', description:'Vista general del negocio.' },
 { id:'management-hours', label:'Horas', path:'/gerencia/horas', icon:'◷', roles:['gerencia'], group:'Análisis', description:'Horas estimadas, registradas y diferencias.' },
 { id:'management-production', label:'Producción', path:'/gerencia/produccion', icon:'▤', roles:['gerencia'], group:'Análisis', description:'Seguimiento global de producción.' },
 { id:'management-finance', label:'Finanzas', path:'/gerencia/finanzas', icon:'＄', roles:['gerencia'], group:'Análisis', description:'Costos, ingresos, gastos y rentabilidad.' },
 { id:'management-kpi', label:'KPI', path:'/gerencia/kpi', icon:'▥', roles:['gerencia'], group:'Análisis', description:'Indicadores y evolución del rendimiento.' },
 { id:'shared-settings', label:'Configuración', path:'/configuracion', icon:'⚙', roles:['comercial','jefa_taller','taller','gerencia'], group:'Sistema', description:'Preferencias disponibles para el perfil.' },
 { id:'admin-navigation', label:'Navegación y permisos', path:'/admin/navegacion', icon:'☷', roles:['gerencia'], group:'Administración', description:'Administra qué roles ven cada interfaz.' },
]
const OVERRIDE_KEY = 'fiancee_navigation_overrides'
export function getOverrides(){ try{return JSON.parse(localStorage.getItem(OVERRIDE_KEY)||'{}')}catch{return {}} }
export function saveOverrides(value){ localStorage.setItem(OVERRIDE_KEY,JSON.stringify(value)) }
export function getAllNavigation(){ const overrides=getOverrides(); return NAVIGATION.map(item=>({...item,...(overrides[item.id]||{}), roles:(overrides[item.id]?.roles ?? item.roles)})) }
export function getNavigationForRole(roleOrRoles){
 const roles = Array.isArray(roleOrRoles) ? roleOrRoles : [roleOrRoles]
 return getAllNavigation().filter(item=>item.enabled!==false && item.roles.some(role=>roles.includes(role)))
}
export function findPage(path){return getAllNavigation().find(item=>item.path===path && item.enabled!==false)}
export function homeForRole(roleOrRoles){
 const roles = Array.isArray(roleOrRoles) ? roleOrRoles : [roleOrRoles]
 const role = roles.find(Boolean)
 return ({comercial:'/comercial',jefa_taller:'/taller',taller:'/trabajador',gerencia:'/gerencia'})[role]||'/'
}
