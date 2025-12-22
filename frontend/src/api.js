const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

// --- Helpers ---

// Recupera el token del almacenamiento local y genera la cabecera
const getAuthHeaders = () => {
  const token = localStorage.getItem('token');
  return token ? { 'Authorization': `Bearer ${token}` } : {};
};

// Variable para evitar bucles infinitos de refresco
let isRefreshing = false;

// Función auxiliar para pedir un nuevo token
const refreshAccessToken = async () => {
  const refreshToken = localStorage.getItem('refresh_token');
  if (!refreshToken) throw new Error('No refresh token available');

  const response = await fetch(`${API_BASE_URL}/auth/refresh`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh_token: refreshToken })
  });

  if (!response.ok) {
    throw new Error('Refresh failed');
  }

  const data = await response.json();
  localStorage.setItem('token', data.access_token); // Guardamos el nuevo token
  return data.access_token;
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
    // CASO 2: Error 401 en Navegación (Token expirado) -> INTENTAR REFRESH
    if (response.status === 401 && !isLoginRequest && !isRefreshing) {
      console.log("Token expirado. Intentando renovar...");
      isRefreshing = true;

      try {
        // 1. Intentamos obtener un token nuevo
        const newToken = await refreshAccessToken();
        isRefreshing = false;
        console.log("Token renovado con éxito. Reintentando petición...");
        window.location.reload(); 
        return;
      } catch (refreshError) {
        console.error("No se pudo renovar la sesión:", refreshError);
        isRefreshing = false;
        // Si falla el refresh, entonces sí cerramos sesión
        localStorage.removeItem('token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user_email');
        window.location.reload();
        throw new Error('Sesión caducada.');
      }
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

export const login = async (email, password) => {
  // FastAPI OAuth2 espera x-www-form-urlencoded, NO JSON
  const formData = new URLSearchParams();
  formData.append('username', email); // El estándar OAuth2 usa 'username' aunque sea email
  formData.append('password', password);

  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded' },
    body: formData,

  });

  // Usamos handleResponse con flag true
  const data = await handleResponse(response, true);
  
  // Guardamos AMBOS tokens
  localStorage.setItem('token', data.access_token);
  localStorage.setItem('refresh_token', data.refresh_token); 
  
  return data;
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