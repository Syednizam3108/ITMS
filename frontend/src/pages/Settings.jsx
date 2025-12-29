import React from 'react'
import { useAppContext } from '../context/AppContext'

export default function Settings() {
  const { user } = useAppContext()

  return (
    <div>
      <h1 className="text-2xl font-semibold mb-4">Settings</h1>
      <div className="bg-white p-4 rounded-lg shadow-md">
        <h2 className="text-lg font-semibold mb-2">User Information</h2>
        <p><strong>Name:</strong> {user?.name || 'N/A'}</p>
        <p><strong>Role:</strong> {user?.role || 'N/A'}</p>
        <p className="mt-4 text-gray-500">
          (Future settings can include changing password, notification preferences, and theme.)
        </p>
      </div>
    </div>
  )
}
