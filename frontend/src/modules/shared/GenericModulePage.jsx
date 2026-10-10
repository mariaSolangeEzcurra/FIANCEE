import { useMemo, useState } from 'react'
import PageHeader from '../../layout/PageHeader.jsx'
import StatCard from '../../components/ui/StatCard.jsx'
import DataTable from '../../components/ui/DataTable.jsx'
import FilterBar from '../../components/ui/FilterBar.jsx'
import EmptyState from '../../components/ui/EmptyState.jsx'

const sampleRows = {
  '/taller/vestidos': [
    {
      id: 'XV-026',
      vestido: 'XV-026 · Verde manzana',
      proceso: 'Bordado',
      estado: 'En proceso',
    },
    {
      id: 'XV-031',
      vestido: 'XV-031 · Crystal',
      proceso: 'Confección',
      estado: 'Pendiente',
    },
  ],
  '/taller/cola': [
    {
      id: 'OT-108',
      vestido: 'XV-026',
      proceso: 'Bordado',
      prioridad: 'Alta',
    },
    {
      id: 'OT-109',
      vestido: 'XV-031',
      proceso: 'Confección',
      prioridad: 'Normal',
    },
  ],
  '/taller/personal': [
    {
      id: 'P-01',
      vestido: 'Equipo de bordado',
      proceso: '7 personas',
      estado: 'Activo',
    },
    {
      id: 'P-02',
      vestido: 'Pruebas',
      proceso: 'Capacidad por confirmar',
      estado: 'Revisar',
    },
  ],
  '/gerencia/horas': [
    {
      id: 'Corte',
      vestido: 'Corte',
      proceso: 'Horas estimadas: por cargar',
      estado: 'Pendiente de datos',
    },
    {
      id: 'Pruebas',
      vestido: 'Pruebas',
      proceso: 'Horas registradas: por cargar',
      estado: 'Pendiente de datos',
    },
  ],
}

export function GenericModulePage({ page }) {
  const [search, setSearch] = useState('')

  const rows = sampleRows[page.path] || []

  const filtered = useMemo(
    () =>
      rows.filter(row =>
        Object.values(row)
          .join(' ')
          .toLowerCase()
          .includes(search.toLowerCase()),
      ),
    [rows, search],
  )

  return (
    <main className="page">
      <PageHeader
        title={page.label}
        description={page.description}
      />

      {['/taller', '/gerencia', '/comercial', '/trabajador'].includes(
        page.path,
      ) && (
        <div className="stats-grid">
          <StatCard
            label="Vestidos activos"
            value="—"
            detail="Pendiente conectar datos reales"
            icon="♧"
          />

          <StatCard
            label="Carga del taller"
            value="—"
            detail="Pendiente conectar datos reales"
            icon="◷"
          />

          <StatCard
            label="Alertas abiertas"
            value="—"
            detail="Pendiente conectar datos reales"
            icon="⚑"
          />
        </div>
      )}

      {rows.length > 0 ? (
        <section className="panel">
          <FilterBar
            search={search}
            setSearch={setSearch}
          />

          <DataTable
            rows={filtered}
            columns={Object.keys(rows[0])
              .filter(key => key !== 'id')
              .map(key => ({
                key,
                label: key.charAt(0).toUpperCase() + key.slice(1),
              }))}
          />
        </section>
      ) : (
        <section className="panel">
          <EmptyState
            title="Estructura de interfaz creada"
            description={`${page.description} Esta pantalla es una base visual; todavía falta conectarla a los endpoints y componentes específicos del prototipo.`}
          />
        </section>
      )}
    </main>
  )
}