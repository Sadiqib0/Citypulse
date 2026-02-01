import { motion } from 'framer-motion';
import { TrendingUp, TrendingDown } from 'lucide-react';

const MetricCard = ({ title, value, icon: Icon, color = 'blue', trend, loading = false }) => {
  const colorClasses = {
    blue: 'from-blue-500 to-blue-600',
    green: 'from-green-500 to-green-600',
    orange: 'from-orange-500 to-orange-600',
    purple: 'from-purple-500 to-purple-600',
    red: 'from-red-500 to-red-600',
  };

  const isPositive = trend && trend.startsWith('+');

  return (
    <motion.div
      whileHover={{ y: -4, scale: 1.02 }}
      transition={{ duration: 0.2 }}
      className="metric-card relative overflow-hidden"
    >
      {/* Background Gradient */}
      <div className="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br opacity-10 rounded-full blur-3xl"
        style={{
          background: `linear-gradient(135deg, ${color === 'blue' ? '#3b82f6' : color === 'green' ? '#10b981' : color === 'orange' ? '#f97316' : color === 'purple' ? '#8b5cf6' : '#ef4444'} 0%, transparent 70%)`
        }}
      />

      <div className="relative z-10">
        {/* Icon */}
        <div className={`inline-flex p-3 rounded-xl bg-gradient-to-br ${colorClasses[color]} shadow-lg mb-4`}>
          <Icon className="w-6 h-6 text-white" />
        </div>

        {/* Title */}
        <h3 className="stat-label mb-2">{title}</h3>

        {/* Value */}
        {loading ? (
          <div className="h-12 w-32 bg-dark-700 animate-pulse rounded-lg"></div>
        ) : (
          <div className="flex items-end justify-between">
            <p className="stat-value">{value}</p>
            
            {/* Trend */}
            {trend && (
              <div className={`flex items-center gap-1 text-sm font-medium ${isPositive ? 'text-green-500' : 'text-red-500'}`}>
                {isPositive ? <TrendingUp className="w-4 h-4" /> : <TrendingDown className="w-4 h-4" />}
                <span>{trend}</span>
              </div>
            )}
          </div>
        )}
      </div>
    </motion.div>
  );
};

export default MetricCard;
