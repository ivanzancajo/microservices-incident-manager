<template>
  <div class="list-container">
    <h2>Gestión de Incidencias</h2>
    
    <div v-if="error" class="error-message">
      Error al cargar incidencias: {{ error.message }}
    </div>

    <div v-if="isLoading" class="loading">Cargando...</div>

    <table v-if="!isLoading && incidents.length > 0">
      <thead>
        <tr>
          <th>ID</th>
          <th>Título</th>
          <th>Estado</th>
          <th>Usuario Asignado</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="incident in incidents" :key="incident.id">
          <td>{{ incident.id }}</td>
          <td>{{ incident.title }}</td>
          <td>{{ incident.status }}</td>
          <td>{{ incident.owner ? incident.owner.name : incident.id_user }}</td>
          <td>
            <button 
              class="btn-edit" 
              @click="emit('edit-incident', incident)"
            >
              Editar
            </button> <button @click="deleteIncident(incident.id)" class="btn-delete">Eliminar</button>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-if="!isLoading && incidents.length === 0" class="no-data">
      No hay incidencias registradas.
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import apiClient from '@/services/api.js';

const emit = defineEmits(['edit-incident']);
const incidents = ref([]);
const isLoading = ref(true);
const error = ref(null);

// --- Función para cargar incidencias ---
const fetchIncidents = async () => {
  isLoading.value = true;
  error.value = null;
  try {
    const response = await apiClient.get('/incidencias');
    incidents.value = response.data;
  } catch (err) {
    console.error("Error al cargar incidencias:", err);
    error.value = err;
  } finally {
    isLoading.value = false;
  }
};

// --- Función para eliminar ---
const deleteIncident = async (id) => {
  if (!confirm('¿Estás seguro de que quieres eliminar esta incidencia?')) {
    return;
  }
  try {
    await apiClient.delete(`/incidencias/${id}`);
    fetchIncidents(); // Recargamos la lista
  } catch (err) {
    console.error(`Error al eliminar incidencia ${id}:`, err);
    alert("Error al eliminar la incidencia.");
  }
};

// --- Cargar datos al montar ---
onMounted(fetchIncidents);

// --- Exponer la función para que App.vue pueda llamarla ---
defineExpose({ fetchIncidents });
</script>

<style scoped>
/* (Puedes reusar los estilos de UserList o copiarlos aquí) */
.list-container {
  font-family: Arial, sans-serif;
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
}
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}
th, td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}
th {
  background-color: #f4f4f4;
}
.btn-delete {
  background-color: #e63946;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
  margin-left: 5px;
}
.btn-edit {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: not-allowed;
}
</style>