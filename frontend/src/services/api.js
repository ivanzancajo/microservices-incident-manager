import axios from 'axios';

// 1. Leemos la variable de entorno para la URL base de la API
const baseURL = import.meta.env.VITE_API_URL;

// 2. Creamos una instancia de Axios
const apiClient = axios.create({
  baseURL: baseURL || 'http://localhost:8000', // URL base de tu API FastAPI
  headers: {
    'Content-Type': 'application/json',
    // Aquí podrías añadir cabeceras de autenticación en el futuro
  }
});

// 3. Exportamos la instancia para usarla en cualquier componente
export default apiClient;