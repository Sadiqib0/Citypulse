/**
 * API service for backend communication
 */
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const WS_BASE_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000';

// Create axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// Events API
export const eventsAPI = {
  getAll: (params = {}) => apiClient.get('/api/v1/events', { params }),
  getById: (id) => apiClient.get(`/api/v1/events/${id}`),
  create: (data) => apiClient.post('/api/v1/events', data),
  update: (id, data) => apiClient.patch(`/api/v1/events/${id}`, data),
  delete: (id) => apiClient.delete(`/api/v1/events/${id}`),
  getStats: () => apiClient.get('/api/v1/events/stats/summary'),
};

// Analytics API
export const analyticsAPI = {
  getOverview: () => apiClient.get('/api/v1/analytics/overview'),
  getTraffic: () => apiClient.get('/api/v1/analytics/traffic'),
  getWeather: () => apiClient.get('/api/v1/analytics/weather'),
  getAnomalies: (sensorId, lookbackMinutes = 60) =>
    apiClient.get('/api/v1/analytics/anomalies', {
      params: { sensor_id: sensorId, lookback_minutes: lookbackMinutes },
    }),
  getPredictions: (eventType, horizonHours = 24) =>
    apiClient.get('/api/v1/analytics/predictions', {
      params: { event_type: eventType, horizon_hours: horizonHours },
    }),
};

// WebSocket connection helper
export class WebSocketClient {
  constructor(endpoint) {
    this.endpoint = endpoint;
    this.ws = null;
    this.listeners = new Map();
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.reconnectDelay = 1000;
  }

  connect() {
    const url = `${WS_BASE_URL}${this.endpoint}`;
    this.ws = new WebSocket(url);

    this.ws.onopen = () => {
      console.log('WebSocket connected:', this.endpoint);
      this.reconnectAttempts = 0;
      this.emit('open');
    };

    this.ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        this.emit('message', data);
      } catch (error) {
        console.error('WebSocket message parse error:', error);
      }
    };

    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      this.emit('error', error);
    };

    this.ws.onclose = () => {
      console.log('WebSocket closed:', this.endpoint);
      this.emit('close');
      this.attemptReconnect();
    };

    return this;
  }

  attemptReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      const delay = this.reconnectDelay * this.reconnectAttempts;
      console.log(`Reconnecting in ${delay}ms... (${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
      
      setTimeout(() => {
        this.connect();
      }, delay);
    } else {
      console.error('Max reconnection attempts reached');
    }
  }

  on(event, callback) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, []);
    }
    this.listeners.get(event).push(callback);
    return this;
  }

  off(event, callback) {
    const callbacks = this.listeners.get(event);
    if (callbacks) {
      const index = callbacks.indexOf(callback);
      if (index > -1) {
        callbacks.splice(index, 1);
      }
    }
    return this;
  }

  emit(event, data) {
    const callbacks = this.listeners.get(event);
    if (callbacks) {
      callbacks.forEach((callback) => callback(data));
    }
  }

  send(data) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    } else {
      console.warn('WebSocket not ready. Message not sent:', data);
    }
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }
}

// Create WebSocket connections
export const createEventsWebSocket = () => new WebSocketClient('/ws/events');
export const createSensorWebSocket = (sensorId) => new WebSocketClient(`/ws/sensors/${sensorId}`);

export default apiClient;
