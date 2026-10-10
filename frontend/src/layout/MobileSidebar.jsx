import Sidebar from './Sidebar.jsx'
export default function MobileSidebar({open,onClose}){if(!open)return null;return <div className="mobile-overlay" onMouseDown={e=>{if(e.target===e.currentTarget)onClose()}}><div className="mobile-drawer"><button className="drawer-close" onClick={onClose} aria-label="Cerrar menú">×</button><Sidebar/></div></div>}
