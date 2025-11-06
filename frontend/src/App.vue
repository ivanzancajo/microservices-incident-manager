<script setup>
import { ref } from 'vue';
import apiClient from './services/api.js'; 
import UserList from './components/UserList.vue';
import UserForm from './components/UserForm.vue';
import IncidentList from './components/IncidentList.vue';
import IncidentForm from './components/IncidentForm.vue';

// --- Lógica de Usuarios ---
const userListComponent = ref(null);
const handleUserCreated = () => {
  if (userListComponent.value) {
    userListComponent.value.fetchUsers();
  }
  if (incidentFormComponent.value) {
    incidentFormComponent.value.fetchUsersForSelect();
  }
};

// --- Lógica de Incidencias ---
const incidentListComponent = ref(null);
const incidentFormComponent = ref(null);

// --- NUEVO: Estado para la incidencia en edición ---
const currentIncidentToEdit = ref(null);

// Esta función se llamará cuando 'IncidentList' emita 'edit-incident'
const handleEditIncident = (incident) => {
  currentIncidentToEdit.value = incident;
};

// Esta función se llamará cuando 'IncidentForm' emita 'incident-saved'
const handleIncidentSaved = () => {
  // 1. Reseteamos la incidencia en edición (para que el form se limpie)
  currentIncidentToEdit.value = null;
  // 2. Refrescamos la lista de incidencias
  if (incidentListComponent.value) {
    incidentListComponent.value.fetchIncidents();
  }
};

const handleDeleteUser = async (userId) => {
  try {
    // 3. La lógica de API se mueve aquí
    await apiClient.delete(`/usuarios/${userId}`);
    
    // 4. Refrescamos TODAS las listas afectadas
    if (userListComponent.value) {
      userListComponent.value.fetchUsers();
    }
    if (incidentListComponent.value) {
      incidentListComponent.value.fetchIncidents();
    }
    if (incidentFormComponent.value) {
      incidentFormComponent.value.fetchUsersForSelect();
    }
    
    alert('Usuario y sus incidencias asociadas eliminados con éxito.');

  } catch (error) {
    console.error(`Error al eliminar usuario ${userId}:`, error);
    alert('Error al eliminar el usuario.');
  }
};
</script>

<template>
  <header>
    <h1>Proyecto de Incidencias</h1>
  </header>

  <main>
    <!-- SECCIÓN DE USUARIOS -->
    <UserForm @user-created="handleUserCreated" />
    <hr class="separator" />

    <!-- 5. ESCUCHAMOS EL NUEVO EVENTO EN UserList -->
    <UserList 
      ref="userListComponent" 
      @delete-user="handleDeleteUser" 
    />

    <hr class="section-divider" />

    <!-- SECCIÓN DE INCIDENCIAS -->
    <IncidentForm 
      ref="incidentFormComponent" 
      :incident-to-edit="currentIncidentToEdit"  
      @incident-saved="handleIncidentSaved" 
    />
    <hr class="separator" />
    <IncidentList 
      ref="incidentListComponent"
      @edit-incident="handleEditIncident"
    />
  </main>
</template>

<style scoped>
header {
  background-color: #f0f0f0;
  padding: 20px;
  text-align: center;
}
main {
  padding: 20px;
}
.separator {
  margin: 30px 0;
  border: 0;
  border-top: 1px solid #eee;
}
.section-divider {
  margin: 60px 0;
  border: 0;
  border-top: 2px solid #005a9c;
}
</style>