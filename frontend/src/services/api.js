import axios from 'axios';

// 1. Leemos la variable de entorno para la URL base de la API
// Esto leerá '/api' desde tus variables de entorno
const baseURL = import.meta.env.VITE_API_URL;

// 2. Creamos una instancia de Axios
const apiClient = axios.create({
  // Si VITE_API_URL no está, usamos '/api' como respaldo
  baseURL: baseURL || '/api', 
  headers: {
    'Content-Type': 'application/json',
  }
});

// 3. Exportamos
export default apiClient;