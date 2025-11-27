<script setup>
import { ref, onMounted } from 'vue';
import { getIncidents, createIncident, updateIncident, deleteIncident, getUsers } from '../api';

const incidents = ref([]);
const users = ref([]);
const newIncident = ref({ title: '', description: '', user_id: null });
const editingIncident = ref(null);
const error = ref(null);
const isLoading = ref(true);

const incidentStatusEnum = ['abierta', 'en_progreso', 'cerrada'];

const fetchIncidents = async () => {
  try {
    isLoading.value = true;
    incidents.value = await getIncidents();
    error.value = null;
  } catch (err) {
    error.value = `Error loading incidents: ${err.message}`;
  } finally {
    isLoading.value = false;
  }
};

const fetchUsers = async () => {
  try {
    users.value = await getUsers();
  } catch (err) {
    error.value = `Error loading users: ${err.message}`;
  }
};

const handleCreateIncident = async () => {
  if (!newIncident.value.title || !newIncident.value.user_id) {
    error.value = 'Title and User are required.';
    return;
  }

  try {
    await createIncident({ ...newIncident.value });
    newIncident.value = { title: '', description: '', user_id: null };
    await fetchIncidents();
  } catch (err) {
    error.value = `Error creating incident: ${err.message}`;
  }
};

const handleUpdateIncident = async (incident) => {
  try {
    await updateIncident(incident.id, { status: incident.status });
    editingIncident.value = null; // Exit edit mode
    await fetchIncidents();
  } catch (err) {
    error.value = `Error updating incident: ${err.message}`;
  }
};

const handleDeleteIncident = async (incidentId) => {
  try {
    await deleteIncident(incidentId);
    await fetchIncidents();
  } catch (err) {
    error.value = `Error deleting incident: ${err.message}`;
  }
};

const getUserName = (userId) => {
  const user = users.value.find(u => u.id === userId);
  return user ? user.name : 'Unknown';
};

onMounted(() => {
  fetchIncidents();
  fetchUsers();
});
</script>

<template>
  <div>
    <h2>Incident Management</h2>

    <!-- Create Incident Form -->
    <form @submit.prevent="handleCreateIncident" class="incident-form">
      <input type="text" v-model="newIncident.title" placeholder="Title" required />
      <input type="text" v-model="newIncident.description" placeholder="Description" />
      <select v-model="newIncident.user_id" required>
        <option :value="null" disabled>Select a user</option>
        <option v-if="users.length === 0" :value="null" disabled>No hay usuarios registrados</option>
        <option v-for="user in users" :key="user.id" :value="user.id">
          {{ user.name }}
        </option>
      </select>
      <button type="submit" class="btn-primary">Create Incident</button>
    </form>

    <div v-if="isLoading">Loading incidents...</div>
    <div v-if="error" class="error">{{ error }}</div>

    <ul v-if="!isLoading && incidents.length">
      <li v-for="incident in incidents" :key="incident.id">
        <div class="incident-details">
          <strong>{{ incident.title }}</strong> (User: {{ getUserName(incident.user_id) }})
          <p>{{ incident.description }}</p>
        </div>
        <div class="incident-actions">
          <select v-model="incident.status" @change="handleUpdateIncident(incident)">
            <option v-for="status in incidentStatusEnum" :value="status" :key="status">
              {{ status }}
            </option>
          </select>
          <button @click="handleDeleteIncident(incident.id)" class="btn-danger">Delete</button>
        </div>
      </li>
    </ul>
    <p v-if="!isLoading && !incidents.length">No incidents found.</p>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap');

:root {
  --primary-color: #5a67d8;
  --danger-color: #e53e3e;
  --background-color: #f7fafc;
  --card-background: #ffffff;
  --text-color: #2d3748;
  --light-gray: #e2e8f0;
  --dark-gray: #718096;
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

.form-group {
  margin-bottom: 1.5rem;
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

.btn-primary, .btn-danger {
  border: none;
  padding: 1rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  width: 100%;
  transition: all 0.3s ease;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
}

.btn-primary {
  background-color: var(--primary-color);
  color: var(--text-color);
}

.btn-primary:hover {
  background-color: #434190;
  color:white;
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

.incident-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
}

.incident-card {
  background-color: var(--card-background);
  border-radius: 12px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: transform 0.3s, box-shadow 0.3s;
}

.incident-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.card-header, .card-body, .card-footer {
  padding: 1.5rem;
}

.card-header {
  border-bottom: 1px solid var(--light-gray);
}

.card-header h3 {
  margin: 0;
  font-weight: 500;
  font-size: 1.25rem;
}

.user-info {
  font-size: 0.9rem;
  color: var(--dark-gray);
  margin-top: 0.25rem;
  display: block;
}

.card-body p {
  color: var(--dark-gray);
  margin: 0;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid var(--light-gray);
  background-color: #fdfdff;
  border-radius: 0 0 12px 12px;
}

.status-select {
  width: auto;
  font-size: 0.9rem;
}

.btn-danger {
  background-color: var(--danger-color);
  color: white;
  width: auto;
}

.btn-danger:hover {
  background-color: #c53030;
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
