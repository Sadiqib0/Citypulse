import { motion, AnimatePresence } from 'framer-motion';
import { AlertCircle, Cloud, Navigation, Wifi, Bell } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';

const eventIcons = {
  traffic: Navigation,
  weather: Cloud,
  sensor: Wifi,
  social: Bell,
  alert: AlertCircle,
};

const severityColors = {
  low: 'text-green-500 bg-green-500/10 border-green-500/20',
  medium: 'text-yellow-500 bg-yellow-500/10 border-yellow-500/20',
  high: 'text-orange-500 bg-orange-500/10 border-orange-500/20',
  critical: 'text-red-500 bg-red-500/10 border-red-500/20',
};

const LiveEventsFeed = ({ events, staticEvents }) => {
  // Combine live and static events
  const allEvents = [...events, ...(staticEvents || [])].slice(0, 20);

  return (
    <div className="card h-[600px] overflow-hidden flex flex-col">
      <div className="flex-1 overflow-y-auto space-y-3 pr-2 scrollbar-thin">
        <AnimatePresence mode="popLayout">
          {allEvents.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-dark-500">
              <Wifi className="w-16 h-16 mb-4 opacity-50" />
              <p>Waiting for live events...</p>
            </div>
          ) : (
            allEvents.map((event, index) => {
              const Icon = eventIcons[event.event_type] || AlertCircle;
              const created = event.created_at || event.timestamp;
              
              return (
                <motion.div
                  key={event.id || `${event.title}-${index}`}
                  initial={{ x: -20, opacity: 0 }}
                  animate={{ x: 0, opacity: 1 }}
                  exit={{ x: 20, opacity: 0 }}
                  transition={{ duration: 0.3 }}
                  className="glass rounded-lg p-4 border border-dark-700/50 hover:border-primary-500/30 transition-all"
                >
                  <div className="flex items-start gap-3">
                    <div className={`p-2 rounded-lg ${severityColors[event.severity || 'low']}`}>
                      <Icon className="w-5 h-5" />
                    </div>
                    
                    <div className="flex-1 min-w-0">
                      <div className="flex items-start justify-between gap-2 mb-1">
                        <h4 className="font-medium text-dark-100 truncate">
                          {event.title}
                        </h4>
                        <span className={`px-2 py-0.5 rounded text-xs font-medium ${severityColors[event.severity || 'low']} whitespace-nowrap`}>
                          {event.severity || 'low'}
                        </span>
                      </div>
                      
                      {event.description && (
                        <p className="text-sm text-dark-400 line-clamp-2 mb-2">
                          {event.description}
                        </p>
                      )}
                      
                      <div className="flex items-center justify-between text-xs text-dark-500">
                        <span className="capitalize">{event.event_type}</span>
                        {created && (
                          <span>
                            {formatDistanceToNow(new Date(created), { addSuffix: true })}
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                </motion.div>
              );
            })
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};

export default LiveEventsFeed;
