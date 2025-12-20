<script setup>
import { ref } from 'vue';
import { login, createUser } from '../api'; // Importamos createUser

const emit = defineEmits(['login-success']);

const email = ref('');
const password = ref('');
const name = ref(''); // Nuevo campo para el registro
const error = ref(null);
const isLoading = ref(false);

// Estado para alternar entre Login y Registro
const isRegistering = ref(false);

const handleSubmit = async () => {
  // Validación básica
  if (!email.value || !password.value || (isRegistering.value && !name.value)) {
    error.value = 'Por favor, rellena todos los campos obligatorios.';
    return;
  }

  try {
    isLoading.value = true;
    error.value = null;

    if (isRegistering.value) {
      // --- LÓGICA DE REGISTRO ---
      
      // 1. Crear el usuario
      // Nota: Enviamos password en texto plano porque el backend lo hashea (ver users-service/crud.py)
      await createUser({
        name: name.value,
        email: email.value,
        password: password.value
      });
      
      // 2. Si se crea bien, hacemos Login automático inmediatamente
      const response = await login(email.value, password.value);
      localStorage.setItem('token', response.access_token);
      localStorage.setItem('user_email', email.value);
      
      emit('login-success');

    } else {
      // --- LÓGICA DE LOGIN NORMAL ---
      const response = await login(email.value, password.value);
      
      localStorage.setItem('token', response.access_token);
      localStorage.setItem('user_email', email.value);

      emit('login-success');
    }

  } catch (err) {
    // Gestionamos mensajes de error específicos
    if (isRegistering.value && err.message.includes('400')) {
      error.value = 'El usuario ya existe. Prueba a iniciar sesión.';
    } else if (!isRegistering.value && err.message.includes('401')) {
      error.value = 'Credenciales incorrectas.';
    } else {
      error.value = err.message || 'Ocurrió un error inesperado.';
    }
    console.error(err);
  } finally {
    isLoading.value = false;
  }
};

// Función para cambiar de modo y limpiar errores
const toggleMode = () => {
  isRegistering.value = !isRegistering.value;
  error.value = null;
  name.value = ''; // Limpiamos nombre al cambiar
};
</script>

<template>
  <div class="login-container">
    <div class="login-card">
      <header>
        <h1>{{ isRegistering ? 'Crear Cuenta' : 'Iniciar Sesión' }}</h1>
        <p class="subtitle">
          {{ isRegistering ? 'Únete al gestor de incidencias' : 'Accede al gestor de incidencias' }}
        </p>
      </header>

      <form @submit.prevent="handleSubmit" class="login-form">
        
        <div v-if="isRegistering" class="form-group slide-down">
          <label for="name">Nombre Completo</label>
          <input 
            id="name"
            type="text" 
            v-model="name" 
            placeholder="Tu nombre" 
            :required="isRegistering"
          />
        </div>

        <div class="form-group">
          <label for="email">Correo Electrónico</label>
          <input 
            id="email"
            type="email" 
            v-model="email" 
            placeholder="ejemplo@empresa.com" 
            required 
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
          {{ isLoading ? 'Procesando...' : (isRegistering ? 'Registrarse' : 'Entrar') }}
        </button>

        <div class="toggle-mode">
          <p>
            {{ isRegistering ? '¿Ya tienes cuenta?' : '¿No tienes cuenta?' }}
            <a href="#" @click.prevent="toggleMode">
              {{ isRegistering ? 'Inicia sesión' : 'Regístrate aquí' }}
            </a>
          </p>
        </div>

      </form>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');

:root {
  --primary-color: #5a67d8;
  --text-color: #2d3748;
}

.login-container {
  font-family: 'Poppins', sans-serif;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
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
  box-sizing: border-box;
}

input:focus {
  outline: none;
  border-color: #5a67d8;
  box-shadow: 0 0 0 3px rgba(90, 103, 216, 0.3);
}

.btn-primary {
  width: 100%;
  padding: 1rem;
  background-color: #5a67d8;
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

/* Estilos para el toggle de modo */
.toggle-mode {
  margin-top: 1.5rem;
  font-size: 0.9rem;
  color: #718096;
}

.toggle-mode a {
  color: #5a67d8;
  font-weight: 600;
  text-decoration: none;
  margin-left: 0.25rem;
  cursor: pointer;
}

.toggle-mode a:hover {
  text-decoration: underline;
}

/* Animación simple para el campo extra */
.slide-down {
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>