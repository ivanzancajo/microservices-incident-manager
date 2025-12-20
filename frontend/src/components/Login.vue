<script setup>
import { ref } from 'vue';
import { login } from '../api'; // Necesitaremos añadir esto a api.js luego

// Definimos los eventos que este componente puede emitir al padre (App.vue)
const emit = defineEmits(['login-success']);

const email = ref('');
const password = ref('');
const error = ref(null);
const isLoading = ref(false);

const handleLogin = async () => {
  if (!email.value || !password.value) {
    error.value = 'Por favor, introduce tu email y contraseña.';
    return;
  }

  try {
    isLoading.value = true;
    error.value = null;

    // Llamamos a la API (implementaremos esta función en el siguiente paso)
    const response = await login(email.value, password.value);
    
    // Guardamos el token
    localStorage.setItem('token', response.access_token);
    localStorage.setItem('user_email', email.value); // Opcional, para mostrarlo

    // Avisamos a App.vue que el login fue correcto
    emit('login-success');

  } catch (err) {
    error.value = 'Credenciales incorrectas o error en el servidor.';
    console.error(err);
  } finally {
    isLoading.value = false;
  }
};
</script>

<template>
  <div class="login-container">
    <div class="login-card">
      <header>
        <h1>Iniciar Sesión</h1>
        <p class="subtitle">Accede al gestor de incidencias</p>
      </header>

      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="email">Correo Electrónico</label>
          <input 
            id="email"
            type="email" 
            v-model="email" 
            placeholder="ejemplo@empresa.com" 
            required 
            autofocus
          />
        </div>

        <div class="form-group">
          <label for="password">Contraseña</label>
          <input 
            id="password"
            type="password" 
            v-model="password" 
            placeholder="••••••••" 
            required 
          />
        </div>

        <div v-if="error" class="error-message">
          <i class="fas fa-exclamation-circle"></i> {{ error }}
        </div>

        <button type="submit" class="btn-primary" :disabled="isLoading">
          {{ isLoading ? 'Entrando...' : 'Entrar' }}
        </button>
      </form>
    </div>
  </div>
</template>

<style scoped>
/* Reutilizando tus variables y estilos para mantener consistencia */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');

:root {
  --primary-color: #5a67d8;
  --text-color: #2d3748;
  --light-gray: #e2e8f0;
  --danger-color: #e53e3e;
}

.login-container {
  font-family: 'Poppins', sans-serif;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh; /* Centrado vertical */
  padding: 1rem;
}

.login-card {
  background-color: white;
  padding: 3rem;
  border-radius: 12px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  width: 100%;
  max-width: 400px;
  text-align: center;
}

header h1 {
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: #718096;
  margin-bottom: 2rem;
  font-size: 0.95rem;
}

.form-group {
  margin-bottom: 1.5rem;
  text-align: left;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #4a5568;
  font-size: 0.9rem;
}

input {
  width: 100%;
  padding: 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.2s;
  box-sizing: border-box; /* Asegura que el padding no rompa el ancho */
}

input:focus {
  outline: none;
  border-color: #5a67d8;
  box-shadow: 0 0 0 3px rgba(90, 103, 216, 0.3);
}

.btn-primary {
  width: 100%;
  padding: 1rem;
  background-color: #5a67d8; /* Usamos el color primario sólido para el botón principal */
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  text-transform: uppercase;
  transition: background-color 0.2s, transform 0.1s;
  margin-top: 1rem;
}

.btn-primary:hover {
  background-color: #434190;
  transform: translateY(-2px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.btn-primary:disabled {
  background-color: #a0aec0;
  cursor: not-allowed;
  transform: none;
}

.error-message {
  background-color: #fed7d7;
  color: #c53030;
  padding: 0.75rem;
  border-radius: 6px;
  font-size: 0.9rem;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  justify-content: center;
}
</style>