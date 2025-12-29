import React from 'react'
import { NavLink } from 'react-router-dom'

const navItems = [
  { path: '/dashboard', label: 'Dashboard' },
  { path: '/live', label: 'Live Feed' },
  { path: '/violations', label: 'Violations' },
  { path: '/add-violation', label: '➕ Add Violation' },
  { path: '/analytics', label: 'Analytics' },
  { path: '/officers', label: 'Officers' },
  { path: '/settings', label: 'Settings' },
]

export default function Sidebar() {
  return (
    <aside className="w-64 bg-gray-800 text-gray-200 flex flex-col">
      <div className="p-4 text-lg font-bold border-b border-gray-700">🚦 Traffic Admin</div>
      <nav className="flex-1 p-4 space-y-2">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `block px-3 py-2 rounded-md text-sm ${
                isActive ? 'bg-gray-700 text-white' : 'hover:bg-gray-700 hover:text-white'
              }`
            }
          >
            {item.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  )
}
