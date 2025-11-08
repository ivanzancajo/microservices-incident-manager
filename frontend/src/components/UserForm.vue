<template>
  <div class="form-container">
    <h3>Añadir Nuevo Usuario</h3>
    
    <form @submit.prevent="handleSubmit">
      
      <!-- Campo Name -->
      <div class="form-group">
        <!-- El 'for' y el 'id' deben ser 'name' -->
        <label for="name">Nombre:</label> 
        <input 
          type="text" 
          id="name" 
          v-model="userData.name" 
          required 
        />
      </div>
      
      <!-- Campo Email -->
      <div class="form-group">
        <label for="email">Email:</label>
        <input 
          type="email" 
          id="email" 
          v-model="userData.email" 
          required 
        />
      </div>

      <button type="submit" :disabled="isLoading">
        {{ isLoading ? 'Creando...' : 'Crear Usuario' }}
      </button>

      <div v-if="error" class="error-message">
        Error al crear usuario: {{ error.message }}
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import apiClient from '@/services/api.js';

// --- Estado del formulario ---
const userData = ref({
  name: '',
  email: ''
  // Si tienes contraseña: password: ''
});

const isLoading = ref(false);
const error = ref(null);

// --- Definir los eventos que este componente puede "emitir" ---
// Usaremos 'user-created' para avisar al componente padre (App.vue)
const emit = defineEmits(['user-created']);

// --- Función de envío ---
const handleSubmit = async () => {
  isLoading.value = true;
  error.value = null;

  try {
    // Usamos el cliente API para hacer el POST 
    await apiClient.post('/usuarios', userData.value);
    
    // 1. Avisamos al padre que hemos creado un usuario
    emit('user-created');

    // 2. Limpiamos el formulario
    userData.value = {
      name: '',
      email: ''
    };
    alert("¡Usuario creado con éxito!");

  } catch (err) {
    console.error("Error al crear usuario:", err);
    error.value = err.response ? err.response.data : err;
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
.form-container {
  max-width: 400px;
  margin: 20px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
}
.form-group {
  margin-bottom: 15px;
}
.form-group label {
  display: block;
  margin-bottom: 5px;
}
.form-group input {
  width: 100%;
  padding: 8px;
  box-sizing: border-box; /* Asegura que el padding no rompa el ancho */
}
button {
  background-color: #28a745;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
button:disabled {
  background-color: #aaa;
}
button:hover:not(:disabled) {
  background-color: #218838;
}
.error-message {
  color: #c00;
  margin-top: 10px;
}
</style>