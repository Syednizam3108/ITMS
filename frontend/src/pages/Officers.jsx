import React, { useState, useEffect } from 'react'
import api from '../utils/api'

export default function Officers() {
  const [officers, setOfficers] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [filterStatus, setFilterStatus] = useState('all')

  useEffect(() => {
    const fetchOfficers = async () => {
      try {
        const res = await api.get('/officers')
        // Backend returns { total, officers } structure
        setOfficers(res.data.officers || [])
      } catch (err) {
        console.error('Error fetching officers:', err)
        setOfficers([])
      } finally {
        setLoading(false)
      }
    }
    fetchOfficers()
  }, [])

  // Filter officers
  const filteredOfficers = officers.filter(officer => {
    const matchesSearch = officer.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         officer.email?.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         officer.badge_number?.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesStatus = filterStatus === 'all' || officer.status === filterStatus
    return matchesSearch && matchesStatus
  })

  // Get status badge styling
  const getStatusBadge = (status) => {
    const styles = {
      active: 'bg-green-100 text-green-800 border border-green-300',
      inactive: 'bg-gray-100 text-gray-800 border border-gray-300',
      pending: 'bg-yellow-100 text-yellow-800 border border-yellow-300',
    }
    return styles[status] || styles.pending
  }

  // Get role badge styling
  const getRoleBadge = (role) => {
    const styles = {
      admin: 'bg-purple-100 text-purple-800 border border-purple-300',
      officer: 'bg-blue-100 text-blue-800 border border-blue-300',
      supervisor: 'bg-teal-100 text-teal-800 border border-teal-300',
    }
    return styles[role] || styles.officer
  }

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Traffic Officers</h1>
        <p className="text-gray-600">Manage and monitor traffic enforcement personnel</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl shadow-lg p-5 text-white">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-blue-100 text-sm font-medium">Total Officers</p>
              <p className="text-3xl font-bold mt-1">{officers.length}</p>
            </div>
            <i className="ri-shield-user-line text-4xl opacity-80"></i>
          </div>
        </div>

        <div className="bg-gradient-to-br from-green-500 to-green-600 rounded-xl shadow-lg p-5 text-white">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-green-100 text-sm font-medium">Active Officers</p>
              <p className="text-3xl font-bold mt-1">
                {officers.filter(o => o.status === 'active').length}
              </p>
            </div>
            <i className="ri-checkbox-circle-line text-4xl opacity-80"></i>
          </div>
        </div>

        <div className="bg-gradient-to-br from-yellow-500 to-yellow-600 rounded-xl shadow-lg p-5 text-white">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-yellow-100 text-sm font-medium">Pending Approval</p>
              <p className="text-3xl font-bold mt-1">
                {officers.filter(o => o.status === 'pending').length}
              </p>
            </div>
            <i className="ri-time-line text-4xl opacity-80"></i>
          </div>
        </div>

        <div className="bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl shadow-lg p-5 text-white">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-purple-100 text-sm font-medium">Administrators</p>
              <p className="text-3xl font-bold mt-1">
                {officers.filter(o => o.role === 'admin').length}
              </p>
            </div>
            <i className="ri-admin-line text-4xl opacity-80"></i>
          </div>
        </div>
      </div>

      {/* Search and Filter */}
      <div className="bg-white rounded-xl shadow-md p-5 mb-6">
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1 relative">
            <i className="ri-search-line absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 text-xl"></i>
            <input
              type="text"
              placeholder="Search by name, email, or officer ID..."
              className="w-full pl-11 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          <select
            className="px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent"
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
          >
            <option value="all">All Status</option>
            <option value="active">Active</option>
            <option value="pending">Pending</option>
            <option value="inactive">Inactive</option>
          </select>
        </div>
      </div>

      {/* Officers Grid */}
      {loading ? (
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-teal-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Loading officers...</p>
          </div>
        </div>
      ) : filteredOfficers.length === 0 ? (
        <div className="bg-white rounded-xl shadow-md p-12 text-center">
          <i className="ri-user-search-line text-6xl text-gray-300 mb-4"></i>
          <p className="text-gray-500 text-lg">No officers found matching your criteria</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredOfficers.map((officer, index) => (
            <div key={index} className="bg-white rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 overflow-hidden border border-gray-100">
              {/* Card Header */}
              <div className="bg-gradient-to-r from-teal-500 to-emerald-500 p-6 text-white">
                <div className="flex items-center justify-between mb-3">
                  <div className="w-16 h-16 bg-white rounded-full flex items-center justify-center">
                    <i className="ri-user-line text-3xl text-teal-600"></i>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-xs font-semibold ${getStatusBadge(officer.status)}`}>
                    {officer.status?.toUpperCase() || 'PENDING'}
                  </span>
                </div>
                <h3 className="text-xl font-bold">{officer.name || 'Unknown Officer'}</h3>
                <p className="text-teal-100 text-sm mt-1">{officer.assigned_zone || 'Traffic Officer'}</p>
              </div>

              {/* Card Body */}
              <div className="p-6 space-y-4">
                <div className="flex items-start gap-3">
                  <i className="ri-shield-star-line text-teal-600 text-xl mt-0.5"></i>
                  <div className="flex-1">
                    <p className="text-xs text-gray-500 uppercase font-medium">Badge Number</p>
                    <p className="text-gray-900 font-semibold">{officer.badge_number || 'N/A'}</p>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <i className="ri-mail-line text-teal-600 text-xl mt-0.5"></i>
                  <div className="flex-1">
                    <p className="text-xs text-gray-500 uppercase font-medium">Email</p>
                    <p className="text-gray-900 text-sm break-all">{officer.email}</p>
                  </div>
                </div>

                {officer.phone && (
                  <div className="flex items-start gap-3">
                    <i className="ri-phone-line text-teal-600 text-xl mt-0.5"></i>
                    <div className="flex-1">
                      <p className="text-xs text-gray-500 uppercase font-medium">Phone</p>
                      <p className="text-gray-900">{officer.phone}</p>
                    </div>
                  </div>
                )}

                <div className="flex items-start gap-3">
                  <i className="ri-building-line text-teal-600 text-xl mt-0.5"></i>
                  <div className="flex-1">
                    <p className="text-xs text-gray-500 uppercase font-medium">Assigned Zone</p>
                    <p className="text-gray-900">{officer.assigned_zone || 'Unassigned'}</p>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <i className="ri-user-star-line text-teal-600 text-xl mt-0.5"></i>
                  <div className="flex-1">
                    <p className="text-xs text-gray-500 uppercase font-medium">Status</p>
                    <span className={`inline-block px-3 py-1 rounded-full text-xs font-semibold ${getStatusBadge(officer.status)}`}>
                      {officer.status?.toUpperCase() || 'PENDING'}
                    </span>
                  </div>
                </div>
              </div>

              {/* Card Footer */}
              <div className="px-6 pb-6 flex gap-2">
                <button className="flex-1 bg-teal-600 hover:bg-teal-700 text-white font-semibold py-2.5 px-4 rounded-lg transition duration-200 flex items-center justify-center gap-2">
                  <i className="ri-edit-line"></i>
                  Edit
                </button>
                <button className="flex-1 bg-gray-100 hover:bg-gray-200 text-gray-700 font-semibold py-2.5 px-4 rounded-lg transition duration-200 flex items-center justify-center gap-2">
                  <i className="ri-eye-line"></i>
                  View
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
