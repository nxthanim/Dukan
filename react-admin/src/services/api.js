import axios from 'axios';

// Base URL - can be configured via environment variable
const BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Create axios instance with base URL
const api = axios.create({
  baseURL: BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Conversations API
export const getConversations = () => api.get('/conversations');
export const getConversation = (id) => api.get(`/conversations/${id}/messages`);
export const flagConversation = (id, needsHuman) => 
  api.post(`/conversations/${id}/flag`, { needsHuman });

// Services API
export const getServices = () => api.get('/api/services');
export const createService = (service) => api.post('/api/services', service);
export const updateService = (id, service) => api.put(`/api/services/${id}`, service);
export const deleteService = (id) => api.delete(`/api/services/${id}`);

// Orders API
export const getOrders = () => api.get('/api/orders');
export const getStats = () => api.get('/api/stats');

// Messages API
export const sendMessage = (chatId, text) => 
  api.post('/api/send-message', { chatId, text });

// Health check
export const healthCheck = () => api.get('/health');

// WebSocket URL
export const getWebSocketUrl = () => {
  const host = window.location.hostname;
  const port = process.env.REACT_APP_WS_PORT || 8000;
  return `ws://${host}:${port}/ws`;
};

export default api;
