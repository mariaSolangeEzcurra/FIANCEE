import { useMemo, useState } from 'react'
import { getAllNavigation, ROLES, saveOverrides } from './navigationConfig.js'

export default function NavigationAdmin() {
  const [items, setItems] = useState(() => getAllNavigation())
  const [selected, setSelected] = useState(items[0]?.id || '')

  const current = items.find(item => item.id === selected)

  const groups = useMemo(
    () => [...new Set(items.map(item => item.group))],
    [items],
  )

  function update(patch) {
    const next = items.map(item =>
      item.id === selected ? { ...item, ...patch } : item,
    )

    setItems(next)

    saveOverrides(
      Object.fromEntries(
        next.map(item => [
          item.id,
          {
            roles: item.roles,
            enabled: item.enabled !== false,
            ...(item.actions ? { actions: item.actions } : {}),
          },
        ]),
      ),
    )
  }

  return (
    <main className="page">
      <header className="page-header">
        <div>
          <span className="eyebrow">ADMINISTRACIÓN</span>
          <h1>Navegación y permisos</h1>
          <p className="muted">
            Configura las interfaces que puede ver cada rol.
          </p>
        </div>

        <span className="badge">Prototipo local</span>
      </header>

      <div className="admin-grid">
        <aside className="panel admin-list">
          <h2>Interfaces</h2>

          {groups.map(group => (
            <div key={group}>
              <p className="nav-group-label">{group}</p>

              {items
                .filter(item => item.group === group)
                .map(item => (
                  <button
                    key={item.id}
                    className={
                      'admin-item ' +
                      (selected === item.id ? 'selected' : '')
                    }
                    onClick={() => setSelected(item.id)}
                  >
                    {item.label}
                    <span>
                      {item.enabled === false ? 'Oculta' : 'Activa'}
                    </span>
                  </button>
                ))}
            </div>
          ))}
        </aside>

        {current && (
          <section className="panel admin-editor">
            <span className="eyebrow">EDITAR INTERFAZ</span>
            <h2>{current.label}</h2>

            <p className="muted">
              Ruta: <code>{current.path}</code>
            </p>

            <label className="switch-row">
              <input
                type="checkbox"
                checked={current.enabled !== false}
                onChange={event =>
                  update({ enabled: event.target.checked })
                }
              />
              Interfaz habilitada
            </label>

            <h3>Roles con acceso</h3>

            {ROLES.map(role => (
              <label className="check-row" key={role.id}>
                <input
                  type="checkbox"
                  checked={current.roles.includes(role.id)}
                  onChange={event =>
                    update({
                      roles: event.target.checked
                        ? [...current.roles, role.id]
                        : current.roles.filter(
                            currentRole => currentRole !== role.id,
                          ),
                    })
                  }
                />
                <span>{role.label}</span>
              </label>
            ))}

            <p className="help-text">
              Los cambios se guardan en el almacenamiento local de este
              navegador. Para producción, hay que guardar permisos en Django y
              validar cada petición en el servidor.
            </p>
          </section>
        )}
      </div>
    </main>
  )
}