import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getMessages = async () => {
  const response = await api.get('/messages');
  return response.data;
};

export const getMessage = async (messageId) => {
  const response = await api.get(`/messages/${messageId}`);
  return response.data;
};

export const getAgentSuggestion = async (messageId) => {
  const response = await api.post(`/agent/suggest/${messageId}`);
  return response.data;
};

export const createDecision = async (decisionData) => {
  const response = await api.post('/decisions', decisionData);
  return response.data;
};

export const getDecisions = async () => {
  const response = await api.get('/decisions');
  return response.data;
};

export const getGraph = async () => {
  const response = await api.get('/graph');
  return response.data;
};

export const resetDemo = async () => {
  const response = await api.post('/reset');
  return response.data;
};

export default api;

