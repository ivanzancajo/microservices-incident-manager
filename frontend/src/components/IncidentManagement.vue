<script setup>
import { ref, onMounted, computed } from 'vue';
import { getIncidents, createIncident, updateIncident, deleteIncident, getUsers } from '../api';

const incidents = ref([]);
const users = ref([]);
const newIncident = ref({ title: '', description: '', user_id: null, status: null });
const editingIncident = ref(null);
const error = ref(null);
const isLoading = ref(true);
const statusDropdownOpen = ref(null);
const userDropdownOpen = ref(false);
const newStatusDropdownOpen = ref(false);

const incidentStatusEnum = ['abierta', 'en_progreso', 'cerrada'];

const incidentStatusDisplay = {
  'abierta': 'Abierta',
  'en_progreso': 'En progreso',
  'cerrada': 'Cerrada'
};

const selectedUserName = computed(() => {
  if (newIncident.value.user_id) {
    const user = users.value.find(u => u.id === newIncident.value.user_id);
    return user ? `${user.name} (${user.email})` : 'Selecciona un usuario';
  }
  return 'Selecciona un usuario';
});

const selectedStatusName = computed(() => {
  if (newIncident.value.status) {
    return incidentStatusDisplay[newIncident.value.status];
  }
  return 'Estado';
});

const statusOrder = {
  'abierta': 1,
  'en_progreso': 2,
  'cerrada': 3,
};

const fetchIncidents = async () => {
  try {
    isLoading.value = true;
    const fetchedIncidents = await getIncidents();
    fetchedIncidents.sort((a, b) => statusOrder[a.status] - statusOrder[b.status]);
    incidents.value = fetchedIncidents;
    error.value = null;
  } catch (err) {
    error.value = `Error al cargar las incidencias: ${err.message}`;
  } finally {
    isLoading.value = false;
  }
};

const fetchUsers = async () => {
  try {
    users.value = await getUsers();
  } catch (err) {
    error.value = `Error al cargar los usuarios: ${err.message}`;
  }
};

const handleCreateIncident = async () => {
  if (!newIncident.value.title || !newIncident.value.user_id || !newIncident.value.status) {
    error.value = 'El título, el usuario y el estado son obligatorios.';
    return;
  }

  try {
    await createIncident({ ...newIncident.value });
    newIncident.value = { title: '', description: '', user_id: null, status: null };
    await fetchIncidents();
  } catch (err) {
    error.value = `Error al crear la incidencia: ${err.message}`;
  }
};

const handleUpdateIncident = async (incident, newStatus) => {
  try {
    await updateIncident(incident.id, { status: newStatus });
    statusDropdownOpen.value = null; // Close dropdown
    await fetchIncidents();
  } catch (err) {
    error.value = `Error al actualizar la incidencia: ${err.message}`;
  }
};

const handleDeleteIncident = async (incidentId) => {
  try {
    await deleteIncident(incidentId);
    await fetchIncidents();
  } catch (err) {
    error.value = `Error al eliminar la incidencia: ${err.message}`;
  }
};

const handleEditClick = (incident) => {
  editingIncident.value = { ...incident };
};

const handleSaveChanges = async () => {
  if (!editingIncident.value) return;

  try {
    await updateIncident(editingIncident.value.id, {
      title: editingIncident.value.title,
      description: editingIncident.value.description,
      user_id: editingIncident.value.user_id
    });
    editingIncident.value = null;
    await fetchIncidents();
  } catch (err) {
    error.value = `Error al guardar los cambios: ${err.message}`;
  }
};

const cancelEdit = () => {
  editingIncident.value = null;
};

const toggleStatusDropdown = (incidentId) => {
  statusDropdownOpen.value = statusDropdownOpen.value === incidentId ? null : incidentId;
};

const toggleUserDropdown = () => {
  userDropdownOpen.value = !userDropdownOpen.value;
};

const selectUser = (userId) => {
  newIncident.value.user_id = userId;
  userDropdownOpen.value = false;
};

const toggleNewStatusDropdown = () => {
  newStatusDropdownOpen.value = !newStatusDropdownOpen.value;
};

const selectNewStatus = (status) => {
  newIncident.value.status = status;
  newStatusDropdownOpen.value = false;
};


const getStatusClass = (status) => {
  return `status-${status.replace('_', '-')}`;
};

//Incorporar el usuario al editar incidencia
const editUserDropdownOpen = ref(false); 


const selectedEditUserName = computed(() => {
  // Verificamos si hay una incidencia en edición y si tiene user_id asignado
  if (editingIncident.value && editingIncident.value.user_id) {
    const user = users.value.find(u => u.id === editingIncident.value.user_id);
    return user ? `${user.name} (${user.email})` : 'Usuario desconocido';
  }
  return 'Selecciona un usuario';
});

// AÑADIR: Funciones para manejar el dropdown de edición
const toggleEditUserDropdown = () => {
  editUserDropdownOpen.value = !editUserDropdownOpen.value;
};

const selectEditUser = (userId) => {
  // Actualizamos el user_id de la incidencia en edición
  editingIncident.value.user_id = userId; 
  editUserDropdownOpen.value = false;
};



onMounted(() => {
  fetchIncidents();
  fetchUsers();
});
</script>

<template>
  <div class="incident-management-container">
    <header>
      <h1>Gestión de Incidencias</h1>
    </header>

    <!-- Create Incident Form -->
    <form @submit.prevent="handleCreateIncident" class="incident-form" v-if="!editingIncident">
      <h3>Añadir Nueva Incidencia</h3>
      <div class="form-group">
        <input type="text" v-model="newIncident.title" placeholder="Título" required />
      </div>
      <div class="form-group">
        <input type="text" v-model="newIncident.description" placeholder="Descripción" />
      </div>
      <div class="form-group">
        <label for="status-dropdown" class="sr-only">Estado</label>
        <div class="custom-dropdown">
          <button id="status-dropdown" @click.prevent="toggleNewStatusDropdown" :class="['dropdown-toggle', { 'placeholder-style': !newIncident.status }]">
            {{ selectedStatusName }}
            <i class="fas fa-chevron-down"></i>
          </button>
          <div v-if="newStatusDropdownOpen" class="dropdown-menu-form">
            <a v-for="status in incidentStatusEnum" :key="status" href="#" @click.prevent="selectNewStatus(status)" class="dropdown-item">
              {{ incidentStatusDisplay[status] }}
            </a>
          </div>
        </div>
      </div>
      <div class="form-group">
        <label for="user-dropdown" class="sr-only">Usuario</label>
        <div class="custom-dropdown">
          <button id="user-dropdown" @click.prevent="toggleUserDropdown" :class="['dropdown-toggle', { 'placeholder-style': !newIncident.user_id }]">
            {{ selectedUserName }}
            <i class="fas fa-chevron-down"></i>
          </button>
          <div v-if="userDropdownOpen" class="dropdown-menu-form">
            <a v-if="users.length === 0" href="#" class="dropdown-item disabled">No hay usuarios registrados</a>
            <a v-for="user in users" :key="user.id" href="#" @click.prevent="selectUser(user.id)" class="dropdown-item">
              {{ user.name }} ({{ user.email }})
            </a>
          </div>
        </div>
      </div>
      <button type="submit" class="btn-primary">Crear Incidencia</button>
    </form>

    <!-- Edit Incident Form -->
    <form v-if="editingIncident" @submit.prevent="handleSaveChanges" class="incident-form">
      <h3>Editar Incidencia</h3>
      <div class="form-group">
        <label>Título</label>
        <input type="text" v-model="editingIncident.title" placeholder="Título" required />
      </div>
      <div class="form-group">
        <label>Descripción</label>
        <input type="text" v-model="editingIncident.description" placeholder="Descripción" />
      </div>
      <div class="form-group">
        <label>Asignar a Usuario</label>
        <div class="custom-dropdown">
          <button @click.prevent="toggleEditUserDropdown" class="dropdown-toggle">
            {{ selectedEditUserName }}
            <i class="fas fa-chevron-down"></i>
          </button>
          
          <div v-if="editUserDropdownOpen" class="dropdown-menu-form">
            <a v-if="users.length === 0" href="#" class="dropdown-item disabled">No hay usuarios disponibles</a>
            <a v-for="user in users" :key="user.id" href="#" @click.prevent="selectEditUser(user.id)" class="dropdown-item">
              {{ user.name }} ({{ user.email }})
            </a>
          </div>
        </div>
      </div>
      <div class="form-actions">
        <button type="submit" class="btn-primary">Guardar Cambios</button>
        <button @click="cancelEdit" type="button" class="btn-secondary">Cancelar</button>
      </div>
    </form>

    <h2 class="list-title">Lista de Incidencias</h2>
    <div v-if="isLoading" class="loading">Cargando incidencias...</div>
    <div v-if="error" class="error">{{ error }}</div>

    <div class="incident-list" v-if="!isLoading && incidents.length">
      <div v-for="incident in incidents" :key="incident.id" class="incident-row-wrapper" :class="{ 'is-active': statusDropdownOpen === incident.id }">
        <div class="incident-card">
          <div class="incident-info">
            <strong class="incident-title">{{ incident.title }}</strong>
            <p class="incident-description">{{ incident.description }}</p>
            <div class="user-assignment">
              <i class="fas fa-user"></i>
              <span>{{ incident.owner ? incident.owner.name : 'Usuario no encontrado' }}</span>
            </div>
          </div>
          <div class="incident-actions">
            <div class="status-dropdown">
              <button @click="toggleStatusDropdown(incident.id)" :class="['status-button', getStatusClass(incident.status)]">
                {{ incidentStatusDisplay[incident.status] }}
                <i class="fas fa-chevron-down"></i>
              </button>
              <div v-if="statusDropdownOpen === incident.id" class="dropdown-menu">
                <a v-for="status in incidentStatusEnum" :key="status" @click.prevent="handleUpdateIncident(incident, status)">
                  {{ incidentStatusDisplay[status] }}
                </a>
              </div>
            </div>
            <button @click="handleDeleteIncident(incident.id)" class="btn-danger">Eliminar</button>
          </div>
        </div>
        <button @click="handleEditClick(incident)" class="btn-edit">
          <i class="fas fa-pencil-alt"></i>
        </button>
      </div>
    </div>
    <p v-if="!isLoading && !incidents.length" class="no-incidents">No se encontraron incidencias. ¡Añade una para empezar!</p>
  </div>
</template>
<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');

:root {
  --primary-color: #5a67d8;
  --danger-color: #e53e3e;
  --background-color: #f7fafc;
  --card-background: #ffffff;
  --text-color: #2d3748;
  --light-gray: #e2e8f0;
  --dark-gray: #718096;
  --secondary-color: #a0aec0;
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}

.incident-management-container {
  font-family: 'Poppins', sans-serif;
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  background-color: var(--background-color);
  color: var(--text-color);
}

header {
  text-align: center;
  margin-bottom: 2.5rem;
}

header h1 {
  font-weight: 600;
  font-size: 2.5rem;
}

.incident-form {
  background-color: var(--card-background);
  padding: 2.5rem;
  border-radius: 12px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  margin-bottom: 2.5rem;
}

.incident-form h3 {
  margin-top: 0;
  margin-bottom: 1.5rem;
  text-align: center;
  font-weight: 500;
  font-size: 1.5rem;
}

.list-title {
  margin-top: 2.5rem;
  margin-bottom: 1.5rem;
  text-align: center;
  font-weight: 500;
  font-size: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: .5rem;
  font-weight: 500;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 2rem;
}

input[type="text"],
select {
  width: 100%;
  padding: 1rem;
  border: 1px solid var(--light-gray);
  border-radius: 8px;
  font-size: 1rem;
  transition: box-shadow 0.2s, border-color 0.2s;
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  background-color: white;
}

select {
  background-image: url('data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22292.4%22%20height%3D%22292.4%22%3E%3Cpath%20fill%3D%22%23718096%22%20d%3D%22M287%2069.4a17.6%2017.6%0A0%200%200-13-5.4H18.4c-5%200-9.3%201.8-12.9%205.4A17.6%2017.6%0A0%200%200%200%2082.2c0%205%201.8%209.3%205.4%2012.9l128%20127.9c3.6%203.6%207.8%205.4%2012.8%205.4s9.2-1.8%2012.8-5.4L287%2095c3.5-3.5%205.4-7.8%205.4-12.8%200-5-1.9-9.2-5.4-12.8z%22%2F%3E%3C%2Fsvg%3E');
  background-repeat: no-repeat;
  background-position: right 1rem center;
  background-size: 0.8em;
  padding-right: 2.5rem;
}

input[type="text"]:focus,
select:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(90, 103, 216, 0.3);
}

.btn-primary, .btn-danger, .btn-edit, .btn-secondary {
  border: none;
  padding: 1rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  transition: all 0.3s ease;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
  text-transform: uppercase;
}

.btn-primary {
  background-color:  rgb(250, 250, 250);
  color:  #434190;
  display: block;
  margin: 1rem auto 0;
  width: 50%;
}

.btn-primary:hover {
  background-color: #434190;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, .1), 0 4px 6px -2px rgba(0, 0, 0, .05);
}

.form-actions .btn-primary {
  width: auto;
  margin: 0;
}

.incident-list {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

.incident-row-wrapper {
  display: flex;
  align-items: center;
  gap: 1rem;
  position: relative;
}

.incident-row-wrapper.is-active {
  z-index: 20;
}

.incident-card {
  background-color: var(--card-background);
  border-radius: 12px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  transition: transform 0.3s, box-shadow 0.3s;
  flex-grow: 1;
}

.incident-card:hover {
  transform: translateY(-1px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

.incident-info {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  flex-grow: 1;
}

.incident-title {
  font-weight: 500;
  font-size: 1.1rem;
}

.incident-description {
  color: var(--dark-gray);
  font-size: 0.9rem;
}

.user-assignment {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--dark-gray);
  font-size: 0.9rem;
  margin-top: auto;
}

.incident-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-shrink: 0;
}

.status-dropdown, .custom-dropdown {
  position: relative;
}

.status-button, .dropdown-toggle {
  display: inline-flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.5rem;
  border: none;
  padding: 0.75rem 1.25rem;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.3s ease;
  width: 100%;
}

.dropdown-toggle {
  background-color: white;
  border: 1px solid var(--light-gray);
  font-size: 1rem;
}

.placeholder-style {
  color: var(--dark-gray);
}

.dropdown-toggle:focus {
  border-color: var(--primary-color);
}

.dropdown-toggle:hover {
  background-color: var(--light-gray);
  color: var(--text-color);
}

.status-button .fa-chevron-down, .dropdown-toggle .fa-chevron-down {
  transition: transform 0.2s;
}

.status-button:hover {
  filter: brightness(95%);
}

.status-abierta {
  background-color: #c6f6d5;
  color: #22543d;
}

.status-en-progreso {
  background-color: #bee3f8;
  color: #2a4365;
}

.status-cerrada {
  background-color: #fed7d7;
  color: #822727;
}

.dropdown-menu, .dropdown-menu-form {
  position: absolute;
  top: calc(100% + 5px);
  right: 0;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -2px rgba(0,0,0,0.05);
  overflow: hidden;
  z-index: 10;
  width: max-content;
}

.dropdown-menu-form {
  width: 100%;
}

.dropdown-menu a, .dropdown-menu-form a {
  display: block;
  padding: 0.75rem 1.5rem;
  color: var(--text-color);
  text-decoration: none;
  cursor: pointer;
  transition: background-color 0.2s;
  /*text-transform: uppercase;*/
}

.dropdown-menu a:hover, .dropdown-menu-form a:hover {
  background-color: var(--light-gray);
}

.dropdown-item.disabled {
  color: var(--dark-gray);
  cursor: default;
  background-color: transparent;
}


.btn-danger {
  background-color: rgb(250, 250, 250);
  color: var(--danger-color);
  width: auto;
}

.btn-danger:hover {
  background-color: var(--danger-color);
  color: white;
  transform: translateY(-2px);
}

.btn-edit {
  background-color: rgb(250, 250, 250);
  color: var(--primary-color);
  width: 40px;
  height: 40px;
  padding: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 8px;
}

.btn-edit:hover {
  background-color: var(--primary-color);
  color: white;
  transform: translateY(-2px);
}

.btn-secondary {
  background-color: rgb(250, 250, 250);
  color: #718096;
}

.btn-secondary:hover {
  background-color: #718096;
  color: white;
  transform: translateY(-2px);
}


.loading, .no-incidents, .error {
  text-align: center;
  padding: 3rem;
  font-size: 1.2rem;
  color: var(--dark-gray);
}

.error {
  color: var(--danger-color);
  background-color: #fed7d7;
  border: 1px solid var(--danger-color);
  border-radius: 8px;
}
</style>
