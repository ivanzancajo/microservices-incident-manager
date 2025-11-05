<template>
  <div class="user-list-container">
    <h2>Gestión de Usuarios</h2>
    
    <div v-if="error" class="error-message">
      Error al cargar los usuarios: {{ error.message }}
    </div>

    <div v-if="isLoading" class="loading">
      Cargando usuarios...
    </div>

    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Nombre</th> <th>Email</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id">
          <td>{{ user.id }}</td>
          <td>{{ user.name }}</td> <td>{{ user.email }}</td>
          <td>
            <button @click="deleteUser(user.id)" class="btn-delete">Eliminar</button>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-if="!isLoading && users.length === 0" class="no-users">
      No hay usuarios registrados.
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import apiClient from '@/services/api.js'; // Importamos nuestro cliente API

// --- Estados del componente ---
const users = ref([]);        // Almacena la lista de usuarios
const isLoading = ref(true);  // Para mostrar un mensaje de "cargando"
const error = ref(null);      // Para almacenar un error si la API falla

// --- Función para cargar usuarios ---
const fetchUsers = async () => {
  isLoading.value = true;
  error.value = null;
  try {
    const response = await apiClient.get('/usuarios');
    users.value = response.data; // Guardamos los datos recibidos
  } catch (err) {
    console.error("Error al cargar usuarios:", err);
    error.value = err;
  } finally {
    isLoading.value = false; // Dejamos de cargar, tanto si hay éxito como si hay error
  }
};

// --- Función para eliminar un usuario ---
// (El enunciado también pide eliminar usuarios [cite: 25])
const deleteUser = async (id) => {
  if (!confirm('¿Estás seguro de que quieres eliminar este usuario?')) {
    return;
  }

  try {
    await apiClient.delete(`/usuarios/${id}`);
    // Después de borrar, actualizamos la lista
    fetchUsers(); 
  } catch (err) {
    console.error(`Error al eliminar usuario ${id}:`, err);
    alert("Error al eliminar el usuario.");
  }
};

// --- Hook del ciclo de vida ---
// onMounted() se ejecuta automáticamente cuando el componente se "monta" (se muestra)
onMounted(() => {
  fetchUsers();
});

defineExpose({ fetchUsers });
</script>

<style scoped>
/* Estilos básicos para que se vea ordenado */
.user-list-container {
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
}

.btn-delete:hover {
  background-color: #c02a35;
}

.error-message {
  color: #c00;
  margin-bottom: 10px;
}

.loading, .no-users {
  text-align: center;
  margin-top: 20px;
  color: #666;
}
</style>