import React from 'react'
import { Routes, Route } from 'react-router-dom'
import Home from '../pages/Home'
import Dashboard from '../pages/Dashboard'
import LiveView from '../pages/LiveView'
import Violations from '../pages/Violations'
import Analytics from '../pages/Analytics'
import Officers from '../pages/Officers'
import Login from '../pages/Login'
import Settings from '../pages/Settings'
import AddViolation from '../pages/AddViolation' // 👈 NEW import

export default function AppRouter() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/live" element={<LiveView />} />
      <Route path="/violations" element={<Violations />} />
      <Route path="/analytics" element={<Analytics />} />
      <Route path="/officers" element={<Officers />} />
      <Route path="/login" element={<Login />} />
      <Route path="/settings" element={<Settings />} />
      <Route path="/add-violation" element={<AddViolation />} /> {/* 👈 NEW route */}
    </Routes>
  )
}
