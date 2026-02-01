import { Cloud, CloudRain, Sun, Wind, Droplets, Eye } from 'lucide-react';
import { motion } from 'framer-motion';

const WeatherWidget = ({ data }) => {
  if (!data) {
    return (
      <div className="card h-64 flex items-center justify-center">
        <div className="text-dark-500">Loading weather data...</div>
      </div>
    );
  }

  const getWeatherIcon = (condition) => {
    const lower = (condition || '').toLowerCase();
    if (lower.includes('rain') || lower.includes('storm')) return CloudRain;
    if (lower.includes('cloud')) return Cloud;
    return Sun;
  };

  const Icon = getWeatherIcon(data.conditions);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="card bg-gradient-to-br from-primary-900/20 to-dark-800/50"
    >
      {/* Current Weather */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-6xl font-bold gradient-text mb-2">
            {Math.round(data.current_temperature || 0)}°
          </h3>
          <p className="text-dark-300 text-lg">{data.conditions || 'Clear'}</p>
          <p className="text-dark-500 text-sm">Feels like {Math.round(data.feels_like || 0)}°</p>
        </div>
        
        <div className="relative">
          <div className="absolute inset-0 bg-primary-500/20 blur-2xl rounded-full"></div>
          <Icon className="w-24 h-24 text-primary-400 relative z-10" />
        </div>
      </div>

      {/* Weather Details */}
      <div className="grid grid-cols-2 gap-4">
        <div className="glass rounded-lg p-3">
          <div className="flex items-center gap-2 text-dark-400 mb-1">
            <Wind className="w-4 h-4" />
            <span className="text-sm">Wind</span>
          </div>
          <p className="text-xl font-semibold text-dark-100">
            {Math.round(data.wind_speed || 0)} km/h
          </p>
        </div>

        <div className="glass rounded-lg p-3">
          <div className="flex items-center gap-2 text-dark-400 mb-1">
            <Droplets className="w-4 h-4" />
            <span className="text-sm">Humidity</span>
          </div>
          <p className="text-xl font-semibold text-dark-100">
            {Math.round(data.humidity || 0)}%
          </p>
        </div>
      </div>

      {/* Weather Alerts */}
      {data.alerts && data.alerts.length > 0 && (
        <div className="mt-4 glass rounded-lg p-3 border border-orange-500/20">
          <h4 className="text-sm font-medium text-orange-400 mb-2">Weather Alerts</h4>
          <ul className="space-y-1">
            {data.alerts.slice(0, 3).map((alert, index) => (
              <li key={index} className="text-sm text-dark-300">• {alert}</li>
            ))}
          </ul>
        </div>
      )}
    </motion.div>
  );
};

export default WeatherWidget;
