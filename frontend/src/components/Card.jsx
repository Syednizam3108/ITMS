import React from 'react'

export default function Card({ title, value, icon }) {
  return (
    <div className="bg-white rounded-lg shadow-md p-4 flex items-center justify-between">
      <div>
        <h3 className="text-sm text-gray-500">{title}</h3>
        <p className="text-2xl font-bold text-gray-700">{value}</p>
      </div>
      <div className="text-gray-400 text-3xl">{icon}</div>
    </div>
  )
}
