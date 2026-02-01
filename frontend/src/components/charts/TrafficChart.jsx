import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts';

const TrafficChart = ({ data }) => {
  if (!data) {
    return (
      <div className="h-64 flex items-center justify-center text-dark-500">
        Loading traffic data...
      </div>
    );
  }

  // Generate hourly data
  const chartData = Array.from({ length: 24 }, (_, hour) => ({
    hour: `${hour.toString().padStart(2, '0')}:00`,
    incidents: data.trends?.hourly_distribution?.[hour] || Math.floor(Math.random() * 10),
    congestion: Math.random() * 100,
  }));

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="glass rounded-lg p-3 border border-dark-700/50 shadow-xl">
          <p className="text-dark-100 font-medium mb-2">{label}</p>
          {payload.map((entry, index) => (
            <p key={index} className="text-sm" style={{ color: entry.color }}>
              {entry.name}: {entry.value.toFixed(1)}
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="space-y-4">
      {/* Traffic Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
        <div className="glass rounded-lg p-4">
          <p className="text-dark-400 text-sm mb-1">Congestion Level</p>
          <div className="flex items-end gap-2">
            <p className="text-3xl font-bold gradient-text">
              {Math.round((data.current_congestion_level || 0) * 100)}%
            </p>
            <div className="flex-1 mb-2">
              <div className="w-full bg-dark-700 rounded-full h-2">
                <div
                  className="bg-gradient-to-r from-orange-500 to-red-500 h-2 rounded-full transition-all duration-500"
                  style={{ width: `${(data.current_congestion_level || 0) * 100}%` }}
                ></div>
              </div>
            </div>
          </div>
        </div>

        <div className="glass rounded-lg p-4">
          <p className="text-dark-400 text-sm mb-1">Average Speed</p>
          <p className="text-3xl font-bold gradient-text">
            {Math.round(data.average_speed || 0)} <span className="text-lg">km/h</span>
          </p>
        </div>

        <div className="glass rounded-lg p-4">
          <p className="text-dark-400 text-sm mb-1">Active Incidents</p>
          <p className="text-3xl font-bold gradient-text">{data.incident_count || 0}</p>
        </div>
      </div>

      {/* Chart */}
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={chartData}>
            <defs>
              <linearGradient id="colorIncidents" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
              </linearGradient>
              <linearGradient id="colorCongestion" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#f97316" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#f97316" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#334155" opacity={0.3} />
            <XAxis 
              dataKey="hour" 
              stroke="#64748b" 
              style={{ fontSize: '12px' }}
              interval={3}
            />
            <YAxis stroke="#64748b" style={{ fontSize: '12px' }} />
            <Tooltip content={<CustomTooltip />} />
            <Legend 
              wrapperStyle={{ paddingTop: '20px' }}
              iconType="circle"
            />
            <Area
              type="monotone"
              dataKey="incidents"
              stroke="#3b82f6"
              strokeWidth={2}
              fillOpacity={1}
              fill="url(#colorIncidents)"
              name="Incidents"
            />
            <Area
              type="monotone"
              dataKey="congestion"
              stroke="#f97316"
              strokeWidth={2}
              fillOpacity={1}
              fill="url(#colorCongestion)"
              name="Congestion %"
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      {/* Affected Areas */}
      {data.affected_areas && data.affected_areas.length > 0 && (
        <div className="glass rounded-lg p-4">
          <h4 className="text-sm font-medium text-dark-300 mb-3">Most Affected Areas</h4>
          <div className="flex flex-wrap gap-2">
            {data.affected_areas.map((area, index) => (
              <span
                key={index}
                className="px-3 py-1 bg-orange-500/10 border border-orange-500/20 text-orange-400 rounded-full text-sm"
              >
                {area}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default TrafficChart;
