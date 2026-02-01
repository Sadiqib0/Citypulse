import { MapContainer, TileLayer, Marker, Popup, CircleMarker } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import { Icon } from 'leaflet';

// Fix for default marker icons in React-Leaflet
delete Icon.Default.prototype._getIconUrl;
Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

const severityColors = {
  low: '#10b981',
  medium: '#eab308',
  high: '#f97316',
  critical: '#ef4444',
};

const CityMap = ({ events }) => {
  const centerPosition = [40.7128, -74.0060]; // New York City

  const getEventColor = (severity) => {
    return severityColors[severity] || severityColors.low;
  };

  return (
    <div className="h-full w-full rounded-2xl overflow-hidden">
      <MapContainer
        center={centerPosition}
        zoom={12}
        style={{ height: '100%', width: '100%' }}
        zoomControl={true}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
        />
        
        {events.map((event, index) => {
          if (!event.latitude || !event.longitude) return null;
          
          const position = [event.latitude, event.longitude];
          const color = getEventColor(event.severity);
          
          return (
            <CircleMarker
              key={event.id || index}
              center={position}
              radius={8}
              pathOptions={{
                fillColor: color,
                fillOpacity: 0.7,
                color: color,
                weight: 2,
                opacity: 0.9,
              }}
            >
              <Popup className="custom-popup">
                <div className="p-2 min-w-[200px]">
                  <h3 className="font-semibold text-lg mb-2 text-dark-100">
                    {event.title}
                  </h3>
                  <p className="text-sm text-dark-300 mb-2">
                    {event.description || 'No description available'}
                  </p>
                  <div className="flex items-center justify-between text-xs">
                    <span className={`px-2 py-1 rounded-full font-medium`}
                      style={{
                        backgroundColor: `${color}20`,
                        color: color,
                        border: `1px solid ${color}40`
                      }}
                    >
                      {event.severity}
                    </span>
                    <span className="text-dark-400 capitalize">{event.event_type}</span>
                  </div>
                </div>
              </Popup>
            </CircleMarker>
          );
        })}
      </MapContainer>
    </div>
  );
};

export default CityMap;
