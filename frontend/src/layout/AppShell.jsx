import { useState } from 'react'
import Sidebar from './Sidebar.jsx'
import MobileSidebar from './MobileSidebar.jsx'
import Topbar from './Topbar.jsx'
export default function AppShell({children}){
    const [open,setOpen]=useState(false);
    return <div className="app-layout"><Sidebar/><div className="app-main">
    <div className="content-area">{children}</div></div><MobileSidebar open={open} onClose={()=>setOpen(false)}/></div>}
