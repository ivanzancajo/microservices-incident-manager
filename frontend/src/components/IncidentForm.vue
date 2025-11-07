<template>
  <div class="form-container">
    <!-- Título dinámico -->
    <h3>{{ isEditing ? 'Editar Incidencia' : 'Registrar Nueva Incidencia' }}</h3>
    
    <form @submit.prevent="handleSubmit">
      
      <!-- CAMPO TÍTULO -->
      <div class="form-group">
        <label for="title">Título:</label>
        <input 
          type="text" 
          id="title" 
          v-model="incidentData.title" 
          required 
        />
      </div>
      
      <!-- CAMPO DESCRIPCIÓN -->
      <div class="form-group">
        <label for="description">Descripción:</label>
        <textarea 
          id="description" 
          v-model="incidentData.description" 
          required
        ></textarea>
      </div>

      <!-- CAMPO ESTADO -->
      <div class="form-group">
        <label for="status">Estado:</label>
        <select id="status" v-model="incidentData.status" required>
          <option value="Abierta">Abierta</option>
          <option value="En Progreso">En Progreso</option>
          <option value="Cerrada">Cerrada</option>
        </select>
      </div>

      <!-- CAMPO USUARIO (Selector) -->
      <div class="form-group">
        <label for="user">Asignar a Usuario:</label>
        <select id="user" v-model="incidentData.id_user" required>
          <option :value="null" disabled>Selecciona un usuario...</option>
          <!-- Itera sobre el array 'users' que se llena con la API -->
          <option v-for="user in users" :key="user.id" :value="user.id">
            {{ user.name }} ({{ user.email }})
          </option>
        </select>
        <div v-if="userError" class="error-message">
          Error al cargar usuarios. Por favor, inténtalo de nuevo.
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

      <!-- MENSAJE DE ERROR -->
      <div v-if="submitError" class="error-message">
        Error al guardar incidencia: {{ submitError.message || submitError }}
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import apiClient from '@/services/api.js';

// --- Diccionario de mapeo (visible → backend) ---
const statusMap = {
  "Abierta": "abierta",
  "En Progreso": "en_progreso",
  "Cerrada": "cerrada"
};

// --- Mapeo inverso (backend → visible) ---
const statusReverseMap = {
  "abierta": "Abierta",
  "en_progreso": "En Progreso",
  "cerrada": "Cerrada"
};

// --- Definir props ---
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
const emit = defineEmits(['incident-saved']);

// --- LÓGICA DE FETCH: Cargar usuarios para el selector ---
const fetchUsersForSelect = async () => {
  userError.value = null; // Limpiar errores
  try {
    // PETICIÓN GET: Asumiendo que el endpoint para listar usuarios es '/usuarios'
    const response = await apiClient.get('/usuarios');
    // Asumiendo que la respuesta exitosa contiene el array de usuarios en 'response.data'
    users.value = response.data;
  } catch (err) {
    console.error("Error fetching users:", err);
    userError.value = err;
  }
};

// Cargar usuarios inmediatamente después de que el componente sea montado
onMounted(fetchUsersForSelect);

// --- Observador (watch) para el modo edición ---
watch(() => props.incidentToEdit, (newIncident) => {
  if (newIncident) {
    // Si recibimos una incidencia, rellenamos el formulario
    isEditing.value = true;
    incidentIdToUpdate.value = newIncident.id;
    
    incidentData.value = {
      title: newIncident.title,
      description: newIncident.description,
      status: statusReverseMap[newIncident.status] || "Abierta",
      user_id: newIncident.id_user // <-- CAMBIO AQUÍ (Lee 'id_user' del prop)
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

// --- Función de envío (Crear o Actualizar) ---
const handleSubmit = async () => {
  isLoading.value = true;
  submitError.value = null;

  try {
    // Traduccion al formato del backend
    const payload = {
      ...incidentData.value,
      status: statusMap[incidentData.value.status] || 'abierta'
    };

    if (isEditing.value) {
      // Lógica de ACTUALIZAR (PUT/PATCH)
      await apiClient.put(
        `/incidencias/${incidentIdToUpdate.value}`, 
        payload
      );
      alert("¡Incidencia actualizada con éxito!");
    } else {
      // Lógica de CREAR (POST)
      await apiClient.post('/incidencias', payload);
      alert("¡Incidencia registrada con éxito!");
    }
    
    emit('incident-saved'); // Notificar al padre para recargar la lista
    resetForm(); // Limpiar el formulario
    isEditing.value = false;
    incidentIdToUpdate.value = null;

  } catch (err) {
    console.error("Error al guardar incidencia:", err);
    // Intentar extraer un mensaje de error útil de la respuesta
    submitError.value = err.response && err.response.data && err.response.data.message 
                        ? { message: err.response.data.message } 
                        : { message: 'Fallo la conexión con el servidor o el servidor devolvió un error desconocido.' };
  } finally {
    isLoading.value = false;
  }
};

// Exponer fetchUsersForSelect (por si el componente padre necesita forzar la recarga)
defineExpose({ fetchUsersForSelect });

</script>

<style scoped>
.form-container {
  max-width: 400px;
  margin: 20px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-family: Arial, sans-serif;
}
h3 {
  text-align: center;
  color: #333;
  margin-bottom: 20px;
}
.form-group {
  margin-bottom: 15px;
}
.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 600;
  color: #555;
}
.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
  box-sizing: border-box; 
  transition: border-color 0.3s;
}
.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  border-color: #007bff;
  outline: none;
}
.form-group textarea {
    resize: vertical;
    min-height: 100px;
}
button {
  background-color: #28a745; /* Color principal */
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.3s;
  margin-top: 10px;
}
button:hover:not(:disabled) {
  background-color: #218838;
}
button:disabled {
  background-color: #aaa;
  cursor: not-allowed;
}
.btn-cancel {
  background-color: #6c757d;
  margin-left: 10px;
}
.btn-cancel:hover {
  background-color: #5a6268;
}
.error-message {
  color: #dc3545;
  background-color: #f8d7da;
  border: 1px solid #f5c6cb;
  padding: 10px;
  border-radius: 6px;
  margin-top: 15px;
  font-size: 0.9em;
}
</style>