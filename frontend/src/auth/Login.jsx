import { useState } from 'react'
import { useAuth } from './AuthContext.jsx'

export default function Login() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [show, setShow] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const { login } = useAuth()

  async function submit(event) {
    event.preventDefault()
    setError('')
    if (!username.trim() || !password) {
      setError('Ingresa tu usuario y contraseña.')
      return
    }
    setLoading(true)
    try {
      await login(username, password)
    } catch (err) {
      setError(err.message || 'No se pudo iniciar sesión.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="login-layout">
      <section className="login-brand">
        <a className="brand" href="/">
          <span className="brand-name">Fiancée</span>
          <span className="brand-caption">ALTA COSTURA · AREQUIPA</span>
        </a>
        <div className="login-quote">
          <p>“Creo que podemos hacerlo.”</p>
          <span>Cada detalle cuenta. Cada vestido tiene una historia.</span>
        </div>
        <small>Gestión integral · Fiancée Alta Costura</small>
      </section>

      <section className="login-content">
        <form className="login-card" onSubmit={submit}>
          <span className="eyebrow">BIENVENIDA</span>
          <h1>Inicia sesión</h1>
          <p className="muted">Ingresa con tu cuenta para continuar.</p>

          <label htmlFor="username">Usuario</label>
          <input id="username" name="username" autoComplete="username" value={username}
            onChange={event => setUsername(event.target.value)} placeholder="Tu usuario" required autoFocus />

          <label htmlFor="password">Contraseña</label>
          <div className="password-field">
            <input id="password" name="password" type={show ? 'text' : 'password'}
              autoComplete="current-password" value={password}
              onChange={event => setPassword(event.target.value)} placeholder="Tu contraseña" required />
            <button type="button" className="text-button" onClick={() => setShow(value => !value)}>
              {show ? 'Ocultar' : 'Mostrar'}
            </button>
          </div>

          {error && <p className="error" role="alert">{error}</p>}
          <button className="button button-primary button-wide" disabled={loading}>
            {loading ? 'Verificando…' : 'Ingresar →'}
          </button>
          <p className="help-text">Si no tienes acceso, solicita una cuenta a la persona administradora.</p>
        </form>
      </section>
    </main>
  )
}
