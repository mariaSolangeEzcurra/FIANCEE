import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './styles/tokens.css'
import './styles/layout.css'
import './styles/responsive.css'
import { Providers } from './app/providers.jsx'
import App from './app/App.jsx'

createRoot(document.getElementById('root')).render(<StrictMode><Providers><App /></Providers></StrictMode>)
