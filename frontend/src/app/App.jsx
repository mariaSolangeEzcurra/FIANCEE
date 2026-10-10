
import { useAuth } from '../auth/AuthContext.jsx'
import Login from '../auth/Login.jsx'
import ProtectedRoute from './ProtectedRoute.jsx'
import { useRouter } from './routes.jsx'
import AppShell from '../layout/AppShell.jsx'
import NavigationAdmin from '../navigation/NavigationAdmin.jsx'
import {
  homeForRole,
  findPage,
} from '../navigation/navigationConfig.js'

import HomeComercial from '../modules/comercial/Home.jsx'
import Contracts from '../modules/comercial/Contracts.jsx'
import Simulator from '../modules/comercial/Simulator.jsx'
import Summary from '../modules/comercial/Summary.jsx'

import HomeTaller from '../modules/taller/Home.jsx'
import Dresses from '../modules/taller/Dresses.jsx'
import ProductionQueue from '../modules/taller/ProductionQueue.jsx'
import Capacity from '../modules/taller/Capacity.jsx'
import Staff from '../modules/taller/Staff.jsx'
import Alerts from '../modules/taller/Alerts.jsx'

import MyDay from '../modules/trabajador/MyDay.jsx'
import LogHours from '../modules/trabajador/LogHours.jsx'
import MyDresses from '../modules/trabajador/MyDresses.jsx'
import MyNotes from '../modules/trabajador/MyNotes.jsx'

import Dashboard from '../modules/gerencia/Dashboard.jsx'
import Hours from '../modules/gerencia/Hours.jsx'
import Production from '../modules/gerencia/Production.jsx'
import KPI from '../modules/gerencia/KPI.jsx'

import Finance from '../modules/shared/Finance.jsx'
import Settings from '../modules/shared/Settings.jsx'

const PAGE_COMPONENTS = {
  '/comercial': HomeComercial,
  '/comercial/contratos': Contracts,
  '/comercial/simulador': Simulator,
  '/comercial/resumen': Summary,

  '/taller': HomeTaller,
  '/taller/vestidos': Dresses,
  '/taller/cola': ProductionQueue,
  '/taller/capacidad': Capacity,
  '/taller/personal': Staff,
  '/taller/alertas': Alerts,

  '/trabajador': MyDay,
  '/trabajador/registrar': LogHours,
  '/trabajador/vestidos': MyDresses,
  '/trabajador/observaciones': MyNotes,

  '/gerencia': Dashboard,
  '/gerencia/horas': Hours,
  '/gerencia/produccion': Production,
  '/gerencia/finanzas': Finance,
  '/gerencia/kpi': KPI,

  '/configuracion': Settings,
}

export default function App() {
  const { session } = useAuth()
  const { path, navigate } = useRouter()

  if (!session) {
    return <Login />
  }

  const roles = session.roles || session.role
  const currentPath = path === '/' ? homeForRole(roles) : path

  if (currentPath === '/admin/navegacion') {
    return (
      <ProtectedRoute path={currentPath}>
        <AppShell>
          <NavigationAdmin />
        </AppShell>
      </ProtectedRoute>
    )
  }

  const page = findPage(currentPath)

  if (!page) {
    return (
      <AppShell>
        <div className="page">
          <span className="eyebrow">PÁGINA NO ENCONTRADA</span>
          <h1>Esta interfaz aún no está configurada</h1>
          <p>Vuelve al inicio o selecciona una opción del menú.</p>

          <button
            className="button button-primary"
            onClick={() => navigate(homeForRole(roles))}
          >
            Ir al inicio
          </button>
        </div>
      </AppShell>
    )
  }

  const PageComponent = PAGE_COMPONENTS[currentPath]

  return (
    <ProtectedRoute path={currentPath}>
      <AppShell>
        {PageComponent ? (
          <PageComponent />
        ) : (
          <div className="page">
            <span className="eyebrow">INTERFAZ PENDIENTE</span>
            <h1>{page.label}</h1>
            <p>
              {page.description} Esta pantalla todavía no tiene un
              componente específico conectado.
            </p>
          </div>
        )}
      </AppShell>
    </ProtectedRoute>
  )
}
