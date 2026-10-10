
import { useEffect, useRef, useState } from 'react'
import { createPortal } from 'react-dom'
import { useAuth } from '../auth/AuthContext.jsx'
import { AppLink, useRouter } from '../app/routes.jsx'
import { getNavigationForRole } from '../navigation/navigationConfig.js'

export default function Sidebar() {
  const { session, logout } = useAuth()
  const { path } = useRouter()

  const [userMenuOpen, setUserMenuOpen] = useState(false)
  const [menuPosition, setMenuPosition] = useState({
    left: 16,
    bottom: 100,
  })

  const userButtonRef = useRef(null)
  const itemsRef = useRef(null)

  const roles = Array.isArray(session?.roles)
    ? session.roles
    : session?.role
      ? [session.role]
      : []

  const items = getNavigationForRole(roles)
  const groups = [...new Set(items.map(item => item.group))]

  const displayName =
    session?.fullName ||
    session?.nombre ||
    session?.username ||
    'Usuario'

  const displayEmail =
    session?.email ||
    session?.correo ||
    ''

  const displayRoles = roles
    .map(role => String(role).replaceAll('_', ' '))
    .join(' · ')

  function toggleUserMenu() {
    if (userMenuOpen) {
      setUserMenuOpen(false)
      return
    }

    const rect = userButtonRef.current?.getBoundingClientRect()

    if (rect) {
      const menuWidth = Math.min(280, window.innerWidth - 24)

      setMenuPosition({
        left: Math.max(
          12,
          Math.min(rect.left, window.innerWidth - menuWidth - 12)
        ),
        bottom: window.innerHeight - rect.top + 8,
      })
    }

    setUserMenuOpen(true)
  }

  useEffect(() => {
    if (!userMenuOpen) return

    function handleKeyDown(event) {
      if (event.key === 'Escape') {
        setUserMenuOpen(false)
      }
    }

    function handleResize() {
      setUserMenuOpen(false)
    }

    window.addEventListener('keydown', handleKeyDown)
    window.addEventListener('resize', handleResize)

    return () => {
      window.removeEventListener('keydown', handleKeyDown)
      window.removeEventListener('resize', handleResize)
    }
  }, [userMenuOpen])

  async function handleLogout() {
    setUserMenuOpen(false)
    await logout()
  }

  const userMenu = userMenuOpen
    ? createPortal(
        <>
          <style>{`
            .fiancee-user-backdrop {
              position: fixed;
              inset: 0;
              z-index: 9998;
              padding: 0;
              border: 0;
              background: transparent;
            }

            .fiancee-user-popup {
              position: fixed;
              z-index: 9999;
              width: 200px;
              max-width: calc(100vw - 24px);
              overflow: hidden;
              border: 1px solid #e9dfdc;
              border-radius: 16px;
              background: #fffdfb;
              box-shadow: 0 12px 30px rgb(40 25 25 / 14%);
              color: #392b2b;
              font-family: inherit;
            }

            .fiancee-user-popup-header {
              padding: 16px 20px;
              border-bottom: 1px solid #eee7e3;
            }

            .fiancee-user-popup-name {
              display: block;
              overflow-wrap: anywhere;
              font-size: 14px;
              font-weight: 600;
            }

            .fiancee-user-popup-email {
              display: block;
              margin-top: 5px;
              overflow-wrap: anywhere;
              color: #857477;
              font-size: 12px;
            }

            .fiancee-user-popup-role {
              display: inline-block;
              margin-top: 12px;
              padding: 5px 12px;
              border-radius: 20px;
              background: #e1edff;
              color: #2455a4;
              font-size: 10px;
              font-weight: 700;
              text-transform: uppercase;
            }

            .fiancee-user-popup-actions {
              padding: 6px 0;
            }

            .fiancee-user-popup-action {
              display: flex;
              align-items: center;
              gap: 12px;
              width: 100%;
              min-height: 44px;
              padding: 10px 20px;
              border: 0;
              border-radius: 0;
              background: transparent;
              color: #48566b;
              font-family: inherit;
              font-size: 14px;
              text-align: left;
              cursor: pointer;
            }

            .fiancee-user-popup-action:hover {
              background: transparent;
            }

            .fiancee-user-popup-logout {
              color: #ef2929;
            }

            .fiancee-user-popup-logout:hover {
              color: #ef2929;
            }

            .fiancee-user-popup-action:focus-visible {
              outline: 2px solid #874c5b;
              outline-offset: -3px;
            }

            .fiancee-user-popup-icon {
              display: inline-flex;
              justify-content: center;
              width: 14px;
              font-size: 17px;
            }
          `}</style>

          <button
            type="button"
            className="fiancee-user-backdrop"
            aria-label="Cerrar menú de usuario"
            onClick={() => setUserMenuOpen(false)}
          />

          <div
            ref={itemsRef}
            className="fiancee-user-popup"
            role="menu"
            style={{
              left: `${menuPosition.left}px`,
              bottom: `${menuPosition.bottom}px`,
            }}
          >
            

            <div className="fiancee-user-popup-actions">
             
              <button
                type="button"
                role="menuitem"
                className="fiancee-user-popup-action fiancee-user-popup-logout"
                onClick={handleLogout}
              >
                <span className="fiancee-user-popup-icon" aria-hidden="true">
                  ⇥
                </span>
                Cerrar sesión
              </button>
            </div>
          </div>
        </>,
        document.body
      )
    : null

  return (
    <>
      <style>{`
        .sidebar {
          display: flex;
          flex-direction: column;
          min-height: 0;
        }

        .sidebar-scroll {
          flex: 1;
          min-height: 0;
          overflow-y: auto;
        }

        .sidebar-footer {
          position: relative;
          z-index: 1;
          flex-shrink: 0;
          margin-top: auto;
          padding: 0.85rem;
          border-top: 1px solid var(--color-border, #e9dfdc);
        }

        .sidebar-user-button {
          display: flex;
          align-items: center;
          gap: 0.7rem;
          width: 100%;
          min-width: 0;
          padding: 0.65rem;
          border: 1px solid transparent;
          border-radius: 10px;
          background: transparent;
          color: inherit;
          font: inherit;
          text-align: left;
          cursor: pointer;
        }

        .sidebar-user-button:hover,
        .sidebar-user-button[aria-expanded="true"] {
          background: transparent;
          border-color: transparent;
          color: inherit;
        }

        .sidebar-user-info {
          display: flex;
          flex: 1;
          flex-direction: column;
          gap: 0.25rem;
          min-width: 0;
        }

        .sidebar-user-info strong,
        .sidebar-user-info small {
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
        }

        .sidebar-user-info strong {
          font-size: 0.84rem;
        }

        .sidebar-user-info small {
          color: var(--color-muted, #857477);
          font-size: 0.72rem;
        }

        .sidebar-user-chevron {
          flex-shrink: 0;
          color: var(--color-muted, #857477);
          font-size: 0.9rem;
        }
      `}</style>

      <aside className="sidebar">
        <a className="brand sidebar-brand" href="/">
          <span className="brand-name">Fiancée</span>
          <span className="brand-caption">ALTA COSTURA</span>
        </a>

        <div className="sidebar-scroll">
          {groups.map(group => (
            <nav className="nav-group" key={group}>
              <p className="nav-group-label">{group}</p>

              {items
                .filter(item => item.group === group)
                .map(item => (
                  <AppLink
                    key={item.id}
                    to={item.path}
                    className={`nav-link ${
                      path === item.path ? 'active' : ''
                    }`}
                  >
                    <span className="nav-icon">{item.icon}</span>
                    <span>{item.label}</span>
                  </AppLink>
                ))}
            </nav>
          ))}
        </div>

        <div className="sidebar-footer">
          <button
            ref={userButtonRef}
            type="button"
            className="sidebar-user-button"
            onClick={toggleUserMenu}
            aria-expanded={userMenuOpen}
            aria-haspopup="menu"
          >
            <span className="avatar">
              {displayName.slice(0, 1).toUpperCase()}
            </span>

            <span className="sidebar-user-info">
              <strong>{displayName}</strong>
              <small>{displayRoles || 'SIN ROL'}</small>
            </span>

            <span className="sidebar-user-chevron" aria-hidden="true">
              {userMenuOpen ? '⌄' : '⌃'}
            </span>
          </button>
        </div>
      </aside>

      {userMenu}
    </>
  )
}
