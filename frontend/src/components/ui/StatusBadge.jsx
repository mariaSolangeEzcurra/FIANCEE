export default function StatusBadge({children,status='neutral'}){return <span className={`status-badge status-${status}`}>{children}</span>}
