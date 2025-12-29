import React, { useEffect, useState } from 'react'
import api from '../utils/api'
import ViolationTable from '../components/ViolationTable'

export default function Violations() {
  const [violations, setViolations] = useState([])

  useEffect(() => {
    const fetchViolations = async () => {
      try {
        const res = await api.get('/violations')
        setViolations(res.data)
      } catch (err) {
        console.error(err)
      }
    }
    fetchViolations()
  }, [])

  return (
    <div>
      <h1 className="text-2xl font-semibold mb-4">All Violations</h1>
      <ViolationTable data={violations} />
    </div>
  )
}
