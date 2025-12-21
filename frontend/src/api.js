const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

// --- Helpers ---

// Recupera el token del almacenamiento local y genera la cabecera
const getAuthHeaders = () => {
  const token = localStorage.getItem('token');
  return token ? { 'Authorization': `Bearer ${token}` } : {};
};

// Manejador de respuestas (igual que antes, pero mejorado para 401)
const handleResponse = async (response, isLoginRequest = false) => {
  if (!response.ok) {
    // CASO 1: Error 401 en el Login (Credenciales malas) -> Solo lanzamos error
    if (response.status === 401 && isLoginRequest) {
      // Intentamos leer el mensaje del backend ("Email o contraseña incorrectos")
      const errorData = await response.json().catch(() => ({ detail: 'Credenciales incorrectas' }));
      throw new Error(errorData.detail);
    }
    // CASO 2: Error 401 en otras rutas (Sesión expirada) -> Limpiamos y recargamos
    if (response.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user_email');
      // Forzamos recarga para volver al login (manera simple de manejarlo)
      window.location.reload();
      throw new Error('Sesión expirada. Por favor, identifícate de nuevo.');
    }
    // CASO 3: Otros errores (500, 404, etc.)
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
    // Pasamos 'true' para indicar que esta es la petición de login
  }).then(res => handleResponse(res, true));
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