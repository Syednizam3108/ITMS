import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Area,
  AreaChart,
  Bar,
  ComposedChart,
} from "recharts";

// Custom Tooltip for better styling
const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-white border-2 border-gray-200 rounded-lg shadow-xl p-4">
        <p className="font-semibold text-gray-800 mb-2">{label}</p>
        {payload.map((entry, index) => (
          <p key={index} style={{ color: entry.color }} className="text-sm font-medium">
            {entry.name}: <span className="font-bold">{entry.value}</span>
          </p>
        ))}
      </div>
    );
  }
  return null;
};

export default function ChartComponent({ data, title }) {
  const showHelmet = title.includes("Helmet") || title.includes("All");
  const showMobile = title.includes("Mobile") || title.includes("Phone") || title.includes("All");
  const showTriple = title.includes("Triple") || title.includes("All");

  return (
    <div className="bg-gradient-to-br from-white to-gray-50 rounded-2xl shadow-xl p-6 border border-gray-100">
      <h3 className="text-xl font-bold mb-6 text-gray-800 flex items-center gap-2">
        <span className="w-1 h-6 bg-gradient-to-b from-blue-500 to-purple-600 rounded-full"></span>
        {title}
      </h3>

      {data.length === 0 ? (
        <p className="text-gray-500">No analytics data available yet.</p>
      ) : (
        <ResponsiveContainer width="100%" height={400}>
          <ComposedChart data={data} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
            <defs>
              <linearGradient id="colorHelmet" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#ef4444" stopOpacity={0.8}/>
                <stop offset="95%" stopColor="#ef4444" stopOpacity={0.1}/>
              </linearGradient>
              <linearGradient id="colorMobile" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#f59e0b" stopOpacity={0.9}/>
                <stop offset="95%" stopColor="#fbbf24" stopOpacity={0.2}/>
              </linearGradient>
              <linearGradient id="colorTriple" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#10b981" stopOpacity={0.8}/>
                <stop offset="95%" stopColor="#10b981" stopOpacity={0.1}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" strokeOpacity={0.5} />
            <XAxis 
              dataKey="date" 
              stroke="#6b7280"
              style={{ fontSize: '12px', fontWeight: '500' }}
            />
            <YAxis 
              allowDecimals={false} 
              stroke="#6b7280"
              style={{ fontSize: '12px', fontWeight: '500' }}
            />
            <Tooltip content={<CustomTooltip />} />
            <Legend 
              wrapperStyle={{ paddingTop: '20px' }}
              iconType="circle"
            />

            {showHelmet && (
              <Area
                type="monotone"
                dataKey="helmet"
                stroke="#ef4444"
                strokeWidth={3}
                fill="url(#colorHelmet)"
                name="No Helmet"
                animationDuration={1500}
                dot={{ fill: '#ef4444', strokeWidth: 2, r: 5 }}
                activeDot={{ r: 8, strokeWidth: 2 }}
              />
            )}
            {showMobile && (
              <Bar
                dataKey="mobile"
                fill="url(#colorMobile)"
                name="Mobile Usage"
                animationDuration={1500}
                radius={[8, 8, 0, 0]}
                stroke="#f59e0b"
                strokeWidth={2}
              />
            )}
            {showTriple && (
              <Area
                type="monotone"
                dataKey="triple"
                stroke="#10b981"
                strokeWidth={3}
                fill="url(#colorTriple)"
                name="Triple Riding"
                animationDuration={1500}
                dot={{ fill: '#10b981', strokeWidth: 2, r: 5 }}
                activeDot={{ r: 8, strokeWidth: 2 }}
              />
            )}
          </ComposedChart>
        </ResponsiveContainer>
      )}
    </div>
  );
}
