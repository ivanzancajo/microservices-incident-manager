<template>
  <div class="form-container">
    <!-- Título dinámico -->
    <h3>{{ isEditing ? 'Editar Incidencia' : 'Registrar Nueva Incidencia' }}</h3>
    
    <form @submit.prevent="handleSubmit">
      
      <!-- CAMPO TÍTULO (Esto faltaba) -->
      <div class="form-group">
        <label for="title">Título:</label>
        <input 
          type="text" 
          id="title" 
          v-model="incidentData.title" 
          required 
        />
      </div>
      
      <!-- CAMPO DESCRIPCIÓN (Esto faltaba) -->
      <div class="form-group">
        <label for="description">Descripción:</label>
        <textarea 
          id="description" 
          v-model="incidentData.description" 
          required
        ></textarea>
      </div>

      <!-- CAMPO ESTADO (Esto faltaba) -->
      <div class="form-group">
        <label for="status">Estado:</label>
        <select id="status" v-model="incidentData.status" required>
          <option value="Abierta">Abierta</option>
          <option value="En Progreso">En Progreso</option>
          <option value="Cerrada">Cerrada</option>
        </select>
      </div>

      <!-- CAMPO USUARIO (Esto faltaba) -->
      <div class="form-group">
        <label for="user">Asignar a Usuario:</label>
        <select id="user" v-model="incidentData.user_id" required>
          <option :value="null" disabled>Selecciona un usuario...</option>
          <option v-for="user in users" :key="user.id" :value="user.id">
            {{ user.name }} ({{ user.email }})
          </option>
        </select>
        <div v-if="userError" class="error-message">
          Error al cargar usuarios.
        </div>
      </div>
      
      <!-- Botón de envío (dinámico) -->
      <button type="submit" :disabled="isLoading">
        {{ isLoading ? 'Guardando...' : (isEditing ? 'Actualizar Incidencia' : 'Registrar Incidencia') }}
      </button>

      <!-- Botón de cancelar (dinámico) -->
      <button 
        type="button" 
        v-if="isEditing" 
        @click="emit('incident-saved')" 
        class="btn-cancel"
      >
        Cancelar
      </button>

      <!-- MENSAJE DE ERROR (Esto faltaba) -->
      <div v-if="submitError" class="error-message">
        Error al crear incidencia: {{ submitError.message }}
      </div>
    </form>
  </div>
</template>

<style scoped>
/* ... (todos tus estilos anteriores) ... */
.btn-cancel {
  background-color: #6c757d;
  margin-left: 10px;
}
.btn-cancel:hover {
  background-color: #5a6268;
}
</style>
<script setup>
import { ref, onMounted, watch } from 'vue'; // <-- Añade 'watch'
import apiClient from '@/services/api.js';

// --- Definir props ---
// 'incidentToEdit' será el objeto que nos pase App.vue
const props = defineProps({
  incidentToEdit: {
    type: Object,
    default: null
  }
});

// --- Estados del formulario ---
const incidentData = ref({
  title: '',
  description: '',
  status: 'Abierta',
  user_id: null
});

const users = ref([]);
const userError = ref(null);
const isLoading = ref(false);
const submitError = ref(null);

// --- Estado de edición ---
const isEditing = ref(false);
const incidentIdToUpdate = ref(null);

// --- Definir eventos ---
// Cambiamos 'incident-created' por 'incident-saved' (más genérico)
const emit = defineEmits(['incident-saved']);

// --- Cargar usuarios (esto no cambia) ---
const fetchUsersForSelect = async () => {
  // ... (tu función fetchUsersForSelect existente) ...
};
onMounted(fetchUsersForSelect);

// --- NUEVO: Observador (watch) ---
// Esto se ejecutará cada vez que 'incidentToEdit' cambie
watch(() => props.incidentToEdit, (newIncident) => {
  if (newIncident) {
    // Si recibimos una incidencia, rellenamos el formulario
    isEditing.value = true;
    incidentIdToUpdate.value = newIncident.id;
    
    incidentData.value = {
      title: newIncident.title,
      description: newIncident.description,
      status: newIncident.status,
      user_id: newIncident.user_id // O newIncident.owner.id si lo tienes
    };
  } else {
    // Si 'incidentToEdit' es null, reseteamos el formulario
    isEditing.value = false;
    incidentIdToUpdate.value = null;
    resetForm();
  }
});

// --- Función para limpiar el formulario ---
const resetForm = () => {
  incidentData.value = {
    title: '',
    description: '',
    status: 'Abierta',
    user_id: null
  };
};

// --- Función de envío (ACTUALIZADA) ---
const handleSubmit = async () => {
  isLoading.value = true;
  submitError.value = null;

  try {
    if (isEditing.value) {
      // --- Lógica de ACTUALIZAR (PUT) ---
      await apiClient.put(
        `/incidentes/${incidentIdToUpdate.value}`, 
        incidentData.value
      );
      alert("¡Incidencia actualizada con éxito!");
    } else {
      // --- Lógica de CREAR (POST) ---
      await apiClient.post('/incidentes', incidentData.value);
      alert("¡Incidencia registrada con éxito!");
    }
    
    emit('incident-saved'); // Avisamos a App.vue
    resetForm(); // Limpiamos el formulario

  } catch (err) {
    console.error("Error al guardar incidencia:", err);
    submitError.value = err.response ? err.response.data : err;
  } finally {
    isLoading.value = false;
    isEditing.value = false; // Reseteamos el modo edición
    incidentIdToUpdate.value = null;
  }
};
</script>

<style scoped>
/* (Puedes reusar los estilos de UserForm o copiarlos aquí) */
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
.form-group input,
.form-group textarea,
.form-group select {
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
.error-message {
  color: #c00;
  margin-top: 10px;
}
</style>