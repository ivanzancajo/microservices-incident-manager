const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

// --- Helpers ---

// Recupera el token del almacenamiento local y genera la cabecera
const getAuthHeaders = () => {
  const token = localStorage.getItem('token');
  return token ? { 'Authorization': `Bearer ${token}` } : {};
};

// Manejador de respuestas (igual que antes, pero mejorado para 401)
const handleResponse = async (response) => {
  if (!response.ok) {
    // Si el token ha expirado o es inválido (401), limpiamos sesión y redirigimos
    if (response.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user_email');
      // Forzamos recarga para volver al login (manera simple de manejarlo)
      window.location.reload();
      throw new Error('Sesión expirada. Por favor, identifícate de nuevo.');
    }
    
    const error = await response.json().catch(() => ({ message: 'Error de red o servidor' }));
    throw new Error(error.detail || error.message);
  }
  
  if (response.status === 204) {
    return;
  }
  return response.json();
};

// --- Auth Service ---

export const login = (email, password) => {
  // FastAPI OAuth2 espera x-www-form-urlencoded, NO JSON
  const formData = new URLSearchParams();
  formData.append('username', email); // El estándar OAuth2 usa 'username' aunque sea email
  formData.append('password', password);

  return fetch(`${API_BASE_URL}/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: formData,
  }).then(handleResponse);
};

// --- Users Service ---

export const getUsers = () => {
  return fetch(`${API_BASE_URL}/users/`, {
    headers: { ...getAuthHeaders() } // Inyectamos token
  }).then(handleResponse);
};

export const createUser = (user) => {
  // Nota: El registro suele ser público, pero si nuestro backend lo va a proteger,
  // descomentar la línea de headers abajo.
  return fetch(`${API_BASE_URL}/users/`, {
    method: 'POST',
    headers: { 
      'Content-Type': 'application/json',
      // ...getAuthHeaders() 
    },
    body: JSON.stringify(user),
  }).then(handleResponse);
};

export const deleteUser = (userId) => {
  return fetch(`${API_BASE_URL}/users/${userId}`, {
    method: 'DELETE',
    headers: { ...getAuthHeaders() } // Inyectamos token
  }).then(handleResponse);
};


// --- Incidents Service ---

export const getIncidents = () => {
  // Esta llamada va al Gateway (BFF). El Gateway debe propagar el header.
  // Nginx ya está configurado para pasar este header al Gateway.
  return fetch(`${API_BASE_URL}/incident-details/`, {
    headers: { ...getAuthHeaders() }
  }).then(handleResponse);
};

export const createIncident = (incident) => {
  return fetch(`${API_BASE_URL}/incidents/`, {
    method: 'POST',
    headers: { 
      'Content-Type': 'application/json',
      ...getAuthHeaders() 
    },
    body: JSON.stringify(incident),
  }).then(handleResponse);
};

export const updateIncident = (incidentId, incident) => {
  return fetch(`${API_BASE_URL}/incidents/${incidentId}`, {
    method: 'PUT',
    headers: { 
      'Content-Type': 'application/json',
      ...getAuthHeaders() 
    },
    body: JSON.stringify(incident),
  }).then(handleResponse);
};

export const deleteIncident = (incidentId) => {
  return fetch(`${API_BASE_URL}/incidents/${incidentId}`, {
    method: 'DELETE',
    headers: { ...getAuthHeaders() }
  }).then(handleResponse);
};