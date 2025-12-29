import React from 'react'
import { Routes, Route } from 'react-router-dom'
import Navbar from './Navbar'
import Sidebar from './Sidebar'
import Dashboard from '../pages/Dashboard'
import LiveView from '../pages/LiveView'
import Violations from '../pages/Violations'
import Analytics from '../pages/Analytics'
import Officers from '../pages/Officers'
import Settings from '../pages/Settings'
import AddViolation from '../pages/AddViolation'

export default function AdminLayout() {
  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar */}
      <Sidebar />

      {/* Main content */}
      <div className="flex-1 flex flex-col">
        <Navbar />
        <main className="flex-1 p-6 overflow-y-auto">
          <Routes>
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/live" element={<LiveView />} />
            <Route path="/violations" element={<Violations />} />
            <Route path="/analytics" element={<Analytics />} />
            <Route path="/officers" element={<Officers />} />
            <Route path="/settings" element={<Settings />} />
            <Route path="/add-violation" element={<AddViolation />} />
            {/* Redirect to dashboard for authenticated users accessing root */}
            <Route path="*" element={<Dashboard />} />
          </Routes>
        </main>
      </div>
    </div>
  )
}
