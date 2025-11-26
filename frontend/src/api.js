const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

// Helper for handling fetch responses
const handleResponse = async (response) => {
  if (!response.ok) {
    const error = await response.json().catch(() => ({ message: 'Network response was not ok' }));
    throw new Error(error.detail || error.message);
  }
  // For 204 No Content, there's no body to parse
  if (response.status === 204) {
    return;
  }
  return response.json();
};

// --- Users Service ---

export const getUsers = () => {
  return fetch(`${API_BASE_URL}/users/usuarios`).then(handleResponse);
};

export const createUser = (user) => {
  return fetch(`${API_BASE_URL}/users/usuarios`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(user),
  }).then(handleResponse);
};

export const deleteUser = (userId) => {
  return fetch(`${API_BASE_URL}/users/usuarios/${userId}`, {
    method: 'DELETE',
  }).then(handleResponse);
};


// --- Incidents Service ---

export const getIncidents = () => {
  return fetch(`${API_BASE_URL}/incidents/incidencias`).then(handleResponse);
};

export const createIncident = (incident) => {
  return fetch(`${API_BASE_URL}/incidents/incidencias`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(incident),
  }).then(handleResponse);
};

export const updateIncident = (incidentId, incident) => {
  return fetch(`${API_BASE_URL}/incidents/incidencias/${incidentId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(incident),
  }).then(handleResponse);
};

export const deleteIncident = (incidentId) => {
  return fetch(`${API_BASE_URL}/incidents/incidencias/${incidentId}`, {
    method: 'DELETE',
  }).then(handleResponse);
};
