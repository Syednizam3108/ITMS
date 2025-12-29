import React from 'react'
import { useAuth } from '../context/AuthContext'

export default function Navbar() {
  const { user, logout } = useAuth()

  return (
    <nav className="bg-white shadow-sm px-6 py-4 flex justify-between items-center">
      <h1 className="text-xl font-semibold text-gray-800">Intelligent Traffic Management</h1>
      <div className="flex items-center gap-4">
        {user && (
          <>
            <div className="flex items-center gap-3">
              <div className="text-right">
                <p className="text-sm font-semibold text-gray-700">{user.full_name}</p>
                <p className="text-xs text-gray-500">{user.role}</p>
              </div>
              <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                <span className="text-blue-600 font-semibold text-lg">
                  {user.full_name?.charAt(0).toUpperCase()}
                </span>
              </div>
            </div>
            <button
              onClick={logout}
              className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
            >
              Logout
            </button>
          </>
        )}
      </div>
    </nav>
  )
}
