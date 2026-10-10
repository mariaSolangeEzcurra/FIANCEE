export default function Topbar({ onMenu }) {
  return (
    <header className="topbar">
      <button
        className="menu-toggle"
        type="button"
        onClick={onMenu}
        aria-label="Abrir menú"
      >
        ☰
      </button>
    </header>
  )
}