import { GenericModulePage } from '../shared/GenericModulePage.jsx'

export default function NavigationPermissions() {
  return (
    <GenericModulePage
      page={{
        label: 'Navegación y permisos',
        description: 'Administración de menús y accesos.',
        path: window.location.pathname,
      }}
    />
  )
}