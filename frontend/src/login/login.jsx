import { useMemo, useState } from 'react'
import '../App.css'

const API_URL = (import.meta.env.VITE_API_URL || 'http://localhost:8000/api').replace(/\/$/, '')

function Login() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [loading, setLoading] = useState(false)
  const [errorMessage, setErrorMessage] = useState('')
  const [session, setSession] = useState(() => {
    try {
      return JSON.parse(sessionStorage.getItem('fiancee_session') || 'null')
    } catch {
      return null
    }
  })

  const currentDate = useMemo(
    () =>
      new Intl.DateTimeFormat('es-PE', {
        weekday: 'long',
        day: '2-digit',
        month: 'long',
      }).format(new Date()),
    [],
  )

  async function handleLogin(event) {
    event.preventDefault()
    setErrorMessage('')

    if (!username.trim() || !password) {
      setErrorMessage('Ingresa tu usuario y contraseña.')
      return
    }

    setLoading(true)

    try {
      const response = await fetch(`${API_URL}/auth/login/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username: username.trim(),
          password,
        }),
      })

      const data = await response.json().catch(() => ({}))

      if (!response.ok) {
        const firstMessage = Object.values(data)
          .flat(Infinity)
          .find((item) => typeof item === 'string')

        setErrorMessage(
          firstMessage ||
            'No se pudo iniciar sesión. Revisa tus credenciales.',
        )
        return
      }

      const newSession = {
        token: data.token,
        username: data.username || username.trim(),
        role: data.rol,
        fullName: data.nombre || data.username || username.trim(),
      }

      sessionStorage.setItem('fiancee_session', JSON.stringify(newSession))
      setSession(newSession)
      setPassword('')
    } catch {
      setErrorMessage(
        'No se pudo conectar con el servidor. Comprueba que el backend esté activo.',
      )
    } finally {
      setLoading(false)
    }
  }

  async function handleLogout() {
    try {
      if (session?.token) {
        await fetch(`${API_URL}/auth/logout/`, {
          method: 'POST',
          headers: {
            Authorization: `Token ${session.token}`,
          },
        })
      }
    } catch {
      // Se limpia la sesión local incluso si no hay conexión.
    }

    sessionStorage.removeItem('fiancee_session')
    setSession(null)
    setUsername('')
    setPassword('')
    setErrorMessage('')
  }

  return (
    <main className={`app-shell ${session ? 'dashboard-shell' : ''}`}>
      <section className="welcome-panel">
        <Brand />

        <div className="quote-block">
          <p className="quote-kicker">
            {session
              ? 'Tu trabajo, con propósito.'
              : '“Creo que podemos hacerlo.”'}
          </p>

          <p className="quote-copy">
            {session
              ? 'Cada detalle cuenta. Cada vestido tiene una historia.'
              : '“Tenemos 47 horas disponibles, el vestido requiere 32 y el proceso crítico tiene 8 libres: es viable con un margen de 6 días.”'}
          </p>
        </div>

        <p className="left-footnote">
          {session
            ? 'Fiancée Alta Costura · Arequipa'
            : `${currentDate.charAt(0).toLocaleUpperCase('es-PE') + currentDate.slice(1)} · Taller A y Taller C`}
        </p>
      </section>

      <section className="content-panel">
        {session ? (
          <div className="dashboard-welcome">
            <span className="eyebrow">ACCESO AUTORIZADO</span>
            <h1>¡Bienvenida!</h1>
            <p className="subtitle">
              Has ingresado a Fiancée Alta Costura.
            </p>

            <div className="session-card">
              <span className="avatar">
                {(session.fullName || 'F').slice(0, 2).toUpperCase()}
              </span>

              <div>
                <strong>{session.fullName}</strong>
                <span>{session.role || 'Personal'}</span>
                <small>@{session.username}</small>
              </div>
            </div>

            <p className="dashboard-note">
              Tu cuenta está autenticada. El siguiente paso será conectar este
              acceso con el panel y las funciones de tu rol.
            </p>

            <button
              className="primary-button"
              type="button"
              onClick={handleLogout}
            >
              Cerrar sesión
            </button>
          </div>
        ) : (
          <div className="login-panel">
            <div className="section-heading login-heading">
              <span className="eyebrow">ACCESO DE PERSONAL</span>
              <h1>Hola{username.trim() ? `, ${username.trim()}` : ''}</h1>
              <p className="subtitle">
                Ingresa con las credenciales asignadas a tu cuenta.
              </p>
            </div>

            <form className="login-form" onSubmit={handleLogin}>
              <label htmlFor="username">Usuario</label>
              <input
                id="username"
                name="username"
                autoComplete="username"
                value={username}
                onChange={(event) => setUsername(event.target.value)}
                placeholder="Tu usuario"
                required
                autoFocus
              />

              <label htmlFor="password">Contraseña</label>
              <div className="password-wrap">
                <input
                  id="password"
                  name="password"
                  type={showPassword ? 'text' : 'password'}
                  autoComplete="current-password"
                  value={password}
                  onChange={(event) => setPassword(event.target.value)}
                  placeholder="Tu contraseña"
                  required
                />

                <button
                  className="show-password"
                  type="button"
                  onClick={() => setShowPassword((value) => !value)}
                >
                  {showPassword ? 'Ocultar' : 'Mostrar'}
                </button>
              </div>

              {errorMessage && (
                <p className="form-error" role="alert">
                  {errorMessage}
                </p>
              )}

              <button
                className="primary-button"
                type="submit"
                disabled={loading}
              >
                {loading ? 'Verificando…' : 'Ingresar'}
                {!loading && <span aria-hidden="true"> →</span>}
              </button>

              <p className="form-help">
                Si no tienes acceso, solicita una cuenta a la persona
                administradora.
              </p>
            </form>
          </div>
        )}
      </section>
    </main>
  )
}

function Brand() {
  return (
    <a className="brand" href="/" aria-label="Fiancée Alta Costura">
      <span className="brand-name">Fiancée</span>
      <span className="brand-caption">ALTA COSTURA · AREQUIPA</span>
    </a>
  )
}

export default Login