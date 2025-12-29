import React from 'react'

export default function ViolationTable({ data }) {
  return (
    <div className="bg-white rounded-lg shadow-md p-4 overflow-x-auto">
      <table className="w-full text-sm text-left text-gray-700">
        <thead className="bg-gray-100">
          <tr>
            <th className="px-4 py-2">Vehicle No</th>
            <th className="px-4 py-2">Violation Type</th>
            <th className="px-4 py-2">Location</th>
            <th className="px-4 py-2">Timestamp</th>
            <th className="px-4 py-2">Evidence</th>
          </tr>
        </thead>
        <tbody>
          {data.length > 0 ? (
            data.map((v, i) => (
              <tr key={i} className="border-b hover:bg-gray-50">
                <td className="px-4 py-2">{v.vehicle_number}</td>
                <td className="px-4 py-2">{v.violation_type}</td>
                <td className="px-4 py-2">{v.location}</td>
                <td className="px-4 py-2">{new Date(v.timestamp).toLocaleString()}</td>
                <td className="px-4 py-2">
                  {v.image_url ? (
                    <a href={v.image_url} target="_blank" className="text-blue-500 hover:underline">
                      View
                    </a>
                  ) : (
                    '—'
                  )}
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="5" className="text-center py-4 text-gray-400">
                No violations found.
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  )
}
