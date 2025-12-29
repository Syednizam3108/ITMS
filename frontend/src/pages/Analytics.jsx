import React, { useState, useEffect } from "react";
import ChartComponent from "../components/ChartComponent";
import api from "../utils/api";

// 📦 Card Component
function Card({ title, value, color, active, onClick }) {
  return (
    <div
      onClick={onClick}
      className={`p-5 rounded-xl shadow-md text-white cursor-pointer transform transition duration-200 ${
        active ? "scale-105 ring-4 ring-blue-300" : ""
      } ${color}`}
    >
      <h3 className="text-lg font-semibold">{title}</h3>
      <p className="text-3xl font-bold mt-2">{value}</p>
    </div>
  );
}

export default function Analytics() {
  const [stats, setStats] = useState({
    total: 0,
    helmet: 0,
    mobile: 0,
    triple: 0,
  });

  const [data, setData] = useState([]);
  const [filteredType, setFilteredType] = useState("All");
  const [loading, setLoading] = useState(false);

  // 🧩 Fetch summary stats
  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await api.get("/stats");
        setStats(res.data);
      } catch (err) {
        console.error("Error fetching stats:", err);
      }
    };
    fetchStats();
  }, []);

  // 🧠 Fetch trend data dynamically (with filter)
  useEffect(() => {
    const fetchTrends = async () => {
      setLoading(true);
      try {
        const endpoint =
          filteredType === "All"
            ? "/stats/dashboard"
            : `/stats/dashboard?type=${encodeURIComponent(filteredType)}`;

        const res = await api.get(endpoint);

        const formattedData = (res.data.trends || []).map((item) => ({
          date: item.date,
          helmet: item.helmet || 0,
          mobile: item.mobile || 0,
          triple: item.triple || 0,
        }));

        setData(formattedData);
      } catch (err) {
        console.error("Error fetching trends:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchTrends();
  }, [filteredType]);

  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      <h1 className="text-2xl font-bold mb-6 text-gray-800">
        Traffic Violation Analytics
      </h1>

      {/* 📊 Summary Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <Card
          title="Total Violations"
          value={stats.total}
          color="bg-blue-600"
          active={filteredType === "All"}
          onClick={() => setFilteredType("All")}
        />
        <Card
          title="Helmet Violations"
          value={stats.helmet}
          color="bg-red-500"
          active={filteredType === "No Helmet Violation"}
          onClick={() => setFilteredType("No Helmet Violation")}
        />
        <Card
          title="Mobile Usage"
          value={stats.mobile}
          color="bg-yellow-500"
          active={filteredType === "Phone Usage While Riding"}
          onClick={() => setFilteredType("Phone Usage While Riding")}
        />
        <Card
          title="Triple Riding"
          value={stats.triple}
          color="bg-green-600"
          active={filteredType === "Triple Riding Violation"}
          onClick={() => setFilteredType("Triple Riding Violation")}
        />
      </div>

      {/* 📈 Chart Section */}
      {loading ? (
        <p className="text-gray-600">Loading data...</p>
      ) : data.length > 0 ? (
        <ChartComponent
          data={data}
          title={`${filteredType} Violation Trends`}
        />
      ) : (
        <p className="text-gray-500">No analytics data available yet.</p>
      )}

      <p className="text-gray-500 mt-4">
        Click on a card above to filter the analytics view by violation type.
      </p>
    </div>
  );
}
