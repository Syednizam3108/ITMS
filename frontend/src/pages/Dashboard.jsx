import React, { useEffect, useState } from "react";

export default function Dashboard() {
  const [violations, setViolations] = useState([]);
  const [filteredViolations, setFilteredViolations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [lastFetched, setLastFetched] = useState(Date.now());
  const [search, setSearch] = useState("");
  const [filterType, setFilterType] = useState("");

  // Fetch violations from backend
  const fetchViolations = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/violations/");
      const data = await response.json();
      // Sort by timestamp (newest first)
      const sorted = data.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
      setViolations(sorted);
      setFilteredViolations(sorted);
      setLastFetched(Date.now());
    } catch (error) {
      console.error("Error fetching violations:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchViolations();
    const interval = setInterval(fetchViolations, 3000); // Auto-refresh every 3s
    return () => clearInterval(interval);
  }, []);

  // 🔍 Filter Logic
  useEffect(() => {
    let filtered = violations;

    if (search.trim()) {
      filtered = filtered.filter((v) =>
        v.vehicle_number.toLowerCase().includes(search.toLowerCase())
      );
    }

    if (filterType) {
      filtered = filtered.filter((v) => v.violation_type === filterType);
    }

    setFilteredViolations(filtered);
  }, [search, filterType, violations]);

  // 🟢 Highlight violations added in last 5 minutes (more visible)
  const isNew = (timestamp) => {
    const timeDiff = (Date.now() - new Date(timestamp).getTime()) / 1000;
    return timeDiff < 300; // last 5 minutes
  };

  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-800">Traffic Violations</h1>
        <p className="text-sm text-gray-500">
          Last updated: {new Date(lastFetched).toLocaleTimeString()}
        </p>
      </div>

      {/* 🔎 Search & Filter Bar */}
      <div className="flex flex-wrap gap-4 mb-6 bg-white p-4 rounded-xl shadow">
        <input
          type="text"
          placeholder="Search by Vehicle Number..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="flex-1 border border-gray-300 rounded-lg px-4 py-2"
        />

        {/* UPDATED DROPDOWN */}
        <select
          value={filterType}
          onChange={(e) => setFilterType(e.target.value)}
          className="border border-gray-300 rounded-lg px-4 py-2"
        >
          <option value="">All Types</option>
          <option value="No Helmet Violation">No Helmet Violation</option>
          <option value="Phone Usage While Riding">Phone Usage While Riding</option>
          <option value="Triple Riding Violation">Triple Riding Violation</option>
        </select>

        <button
          onClick={() => {
            setSearch("");
            setFilterType("");
          }}
          className="bg-gray-700 text-white px-4 py-2 rounded-lg hover:bg-gray-800"
        >
          Reset
        </button>
      </div>

      {/* 🧾 Violations Table */}
      {loading ? (
        <p className="text-center py-8">Loading violations...</p>
      ) : (
        <div className="overflow-x-auto bg-white shadow-md rounded-xl p-4">
          <table className="min-w-full table-auto">
            <thead>
              <tr className="bg-gray-200 text-left text-sm font-semibold text-gray-700">
                <th className="py-3 px-4">Vehicle Number</th>
                <th className="py-3 px-4">Violation Type</th>
                <th className="py-3 px-4">Fine Amount</th>
                <th className="py-3 px-4">Confidence</th>
                <th className="py-3 px-4">Timestamp</th>
                <th className="py-3 px-4">Image</th>
              </tr>
            </thead>
            <tbody>
              {filteredViolations.length > 0 ? (
                filteredViolations.map((v, index) => (
                  <tr
                    key={v.id || index}
                    className={`border-b hover:bg-gray-50 transition ${
                      isNew(v.timestamp) ? "bg-green-50 border-l-4 border-green-500" : ""
                    }`}
                  >
                    <td className="py-3 px-4 font-semibold text-gray-800">
                      {v.vehicle_number}
                    </td>
                    <td className="py-3 px-4">
                      <div className="flex items-center gap-2">
                        <span className="text-gray-700">{v.violation_type}</span>
                        {isNew(v.timestamp) && (
                          <span className="text-xs bg-green-500 text-white px-2 py-1 rounded-full animate-pulse">
                            🔴 LIVE
                          </span>
                        )}
                      </div>
                    </td>
                    <td className="py-3 px-4 font-semibold text-red-600">
                      ₹{v.fine_amount}
                    </td>
                    <td className="py-3 px-4">
                      {v.confidence ? (
                        <span className={`px-2 py-1 rounded text-xs font-semibold ${
                          v.confidence > 0.7 ? 'bg-green-100 text-green-700' : 
                          v.confidence > 0.5 ? 'bg-yellow-100 text-yellow-700' : 
                          'bg-red-100 text-red-700'
                        }`}>
                          {(v.confidence * 100).toFixed(1)}%
                        </span>
                      ) : '—'}
                    </td>
                    <td className="py-3 px-4 text-gray-600 text-sm">
                      {new Date(v.timestamp).toLocaleString()}
                    </td>
                    <td className="py-3 px-4">
                      {v.image_path ? (
                        <img
                          src={`http://127.0.0.1:8000${v.image_path}`}
                          alt="violation"
                          className="w-24 h-24 object-cover rounded-md border shadow-sm hover:scale-150 transition-transform cursor-pointer"
                          onClick={() => window.open(`http://127.0.0.1:8000${v.image_path}`, '_blank')}
                        />
                      ) : (
                        <span className="text-gray-400">No image</span>
                      )}
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="6" className="text-center py-8 text-gray-500">
                    No violations found.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
