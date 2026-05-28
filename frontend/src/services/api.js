import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth endpoints - NOTE: Use /login/ not /token/
export const login = (credentials) => api.post('/login/', credentials);
export const getProfile = () => api.get('/users/profile/');

// User endpoints
export const getUsers = () => api.get('/users/');
export const createUser = (data) => api.post('/users/', data);
export const updateUser = (id, data) => api.patch(`/users/${id}/`, data);
export const deleteUser = (id) => api.delete(`/users/${id}/`);

// Project endpoints
export const getProjects = () => api.get('/projects/');
export const createProject = (data) => api.post('/projects/', data);
export const updateProject = (id, data) => api.put(`/projects/${id}/`, data);
export const deleteProject = (id) => api.delete(`/projects/${id}/`);

// Task endpoints
export const getTasks = () => api.get('/tasks/');
export const createTask = (data) => api.post('/tasks/', data);
export const updateTask = (id, data) => api.put(`/tasks/${id}/`, data);
export const deleteTask = (id) => api.delete(`/tasks/${id}/`);
export const markTaskComplete = (id) => api.post(`/tasks/${id}/mark_complete/`);
export const verifyTask = (id, data) => api.post(`/tasks/${id}/verify/`, data);
export const resubmitTask = (id, data) => api.post(`/tasks/${id}/resubmit/`, data);

// Dashboard endpoints
export const getDashboardStats = () => api.get('/dashboard/stats/');

export default api;
