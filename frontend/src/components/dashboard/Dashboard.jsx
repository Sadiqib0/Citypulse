import { useState, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { motion } from 'framer-motion';
import { 
  Activity, 
  AlertTriangle, 
  Cloud, 
  Navigation, 
  TrendingUp,
  Wifi,
  MapPin,
  Zap
} from 'lucide-react';
import { analyticsAPI, eventsAPI, createEventsWebSocket } from '../../services/api';
import MetricCard from './MetricCard';
import LiveEventsFeed from './LiveEventsFeed';
import TrafficChart from '../charts/TrafficChart';
import WeatherWidget from './WeatherWidget';
import CityMap from '../maps/CityMap';

const Dashboard = () => {
  const [liveEvents, setLiveEvents] = useState([]);
  const [wsConnected, setWsConnected] = useState(false);

  // Fetch analytics overview
  const { data: overview, isLoading: overviewLoading } = useQuery({
    queryKey: ['analytics-overview'],
    queryFn: async () => {
      const response = await analyticsAPI.getOverview();
      return response.data;
    },
    refetchInterval: 30000,
  });

  // Fetch traffic analytics
  const { data: traffic } = useQuery({
    queryKey: ['traffic-analytics'],
    queryFn: async () => {
      const response = await analyticsAPI.getTraffic();
      return response.data;
    },
    refetchInterval: 30000,
  });

  // Fetch weather analytics
  const { data: weather } = useQuery({
    queryKey: ['weather-analytics'],
    queryFn: async () => {
      const response = await analyticsAPI.getWeather();
      return response.data;
    },
    refetchInterval: 60000,
  });

  // Fetch recent events
  const { data: events } = useQuery({
    queryKey: ['recent-events'],
    queryFn: async () => {
      const response = await eventsAPI.getAll({ limit: 50 });
      return response.data;
    },
    refetchInterval: 15000,
  });

  // WebSocket connection for live updates
  useEffect(() => {
    const ws = createEventsWebSocket();
    
    ws.on('open', () => {
      setWsConnected(true);
    });

    ws.on('message', (data) => {
      if (data.data) {
        setLiveEvents((prev) => [data.data, ...prev].slice(0, 100));
      }
    });

    ws.on('close', () => {
      setWsConnected(false);
    });

    ws.connect();

    return () => {
      ws.disconnect();
    };
  }, []);

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
      },
    },
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: {
        duration: 0.5,
      },
    },
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-dark-900 via-dark-800 to-dark-900">
      {/* Header */}
      <header className="glass border-b border-dark-700/50 sticky top-0 z-50 backdrop-blur-xl">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="bg-gradient-to-br from-primary-500 to-primary-600 p-3 rounded-xl shadow-lg">
                <Activity className="w-8 h-8 text-white" />
              </div>
              <div>
                <h1 className="text-3xl font-bold gradient-text">CityPulse</h1>
                <p className="text-dark-400 text-sm">Real-Time Analytics Platform</p>
              </div>
            </div>
            
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2 px-4 py-2 glass rounded-lg">
                <div className={`w-2 h-2 rounded-full ${wsConnected ? 'bg-green-500' : 'bg-red-500'} animate-pulse`}></div>
                <span className="text-sm text-dark-300">
                  {wsConnected ? 'Live' : 'Disconnected'}
                </span>
              </div>
              <button className="btn-secondary flex items-center gap-2">
                <Zap className="w-4 h-4" />
                Settings
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-8">
        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          className="space-y-8"
        >
          {/* Key Metrics */}
          <motion.div variants={itemVariants}>
            <h2 className="section-title mb-6 flex items-center gap-2">
              <TrendingUp className="w-6 h-6" />
              Key Metrics
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <MetricCard
                title="Total Events"
                value={overview?.total_events || 0}
                icon={Activity}
                color="blue"
                trend="+12%"
                loading={overviewLoading}
              />
              <MetricCard
                title="Active Sensors"
                value={overview?.active_sensors || 0}
                icon={Wifi}
                color="green"
                trend="+5%"
                loading={overviewLoading}
              />
              <MetricCard
                title="Unresolved Alerts"
                value={overview?.unresolved_alerts || 0}
                icon={AlertTriangle}
                color="orange"
                trend="-8%"
                loading={overviewLoading}
              />
              <MetricCard
                title="Avg Sensor Value"
                value={overview?.avg_sensor_value?.toFixed(1) || '0.0'}
                icon={Navigation}
                color="purple"
                trend="+3%"
                loading={overviewLoading}
              />
            </div>
          </motion.div>

          {/* Main Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Left Column - 2/3 width */}
            <div className="lg:col-span-2 space-y-6">
              {/* City Map */}
              <motion.div variants={itemVariants}>
                <h2 className="section-title mb-4 flex items-center gap-2">
                  <MapPin className="w-6 h-6" />
                  Live City Map
                </h2>
                <div className="card h-96">
                  <CityMap events={events || []} />
                </div>
              </motion.div>

              {/* Traffic Analysis */}
              <motion.div variants={itemVariants}>
                <h2 className="section-title mb-4 flex items-center gap-2">
                  <Activity className="w-6 h-6" />
                  Traffic Analysis
                </h2>
                <div className="card">
                  <TrafficChart data={traffic} />
                </div>
              </motion.div>
            </div>

            {/* Right Column - 1/3 width */}
            <div className="space-y-6">
              {/* Weather Widget */}
              <motion.div variants={itemVariants}>
                <h2 className="section-title mb-4 flex items-center gap-2">
                  <Cloud className="w-6 h-6" />
                  Weather
                </h2>
                <WeatherWidget data={weather} />
              </motion.div>

              {/* Live Events Feed */}
              <motion.div variants={itemVariants}>
                <h2 className="section-title mb-4 flex items-center gap-2">
                  <Zap className="w-6 h-6" />
                  Live Events
                </h2>
                <LiveEventsFeed events={liveEvents} staticEvents={events || []} />
              </motion.div>
            </div>
          </div>

          {/* Event Distribution */}
          <motion.div variants={itemVariants}>
            <h2 className="section-title mb-4">Event Distribution</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
              {overview?.event_distribution && Object.entries(overview.event_distribution).map(([type, count]) => (
                <div key={type} className="card-hover">
                  <div className="flex items-center justify-between">
                    <span className="text-dark-400 capitalize">{type}</span>
                    <span className="text-2xl font-bold gradient-text">{count}</span>
                  </div>
                  <div className="mt-2 w-full bg-dark-700 rounded-full h-2">
                    <div
                      className="bg-gradient-to-r from-primary-600 to-primary-500 h-2 rounded-full transition-all duration-500"
                      style={{ width: `${Math.min((count / (overview?.total_events || 1)) * 100, 100)}%` }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>
          </motion.div>
        </motion.div>
      </main>

      {/* Footer */}
      <footer className="mt-16 py-8 border-t border-dark-800">
        <div className="max-w-7xl mx-auto px-6 text-center">
          <p className="text-dark-500 text-sm">
            CityPulse © 2024 - Real-Time Event & Analytics Platform
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Dashboard;
