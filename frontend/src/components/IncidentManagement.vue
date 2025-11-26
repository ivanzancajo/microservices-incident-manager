<script setup>
import { ref, onMounted } from 'vue';
import { getIncidents, createIncident, updateIncident, deleteIncident } from '../api';

const incidents = ref([]);
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

const handleCreateIncident = async () => {
  if (!newIncident.value.title || !newIncident.value.user_id) {
    error.value = 'Title and User ID are required.';
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

onMounted(fetchIncidents);
</script>

<template>
  <div>
    <h2>Incident Management</h2>

    <!-- Create Incident Form -->
    <form @submit.prevent="handleCreateIncident" class="incident-form">
      <input type="text" v-model="newIncident.title" placeholder="Title" required />
      <input type="text" v-model="newIncident.description" placeholder="Description" />
      <input type="number" v-model.number="newIncident.user_id" placeholder="User ID" required />
      <button type="submit">Create Incident</button>
    </form>

    <div v-if="isLoading">Loading incidents...</div>
    <div v-if="error" class="error">{{ error }}</div>

    <ul v-if="!isLoading && incidents.length">
      <li v-for="incident in incidents" :key="incident.id">
        <div class="incident-details">
          <strong>{{ incident.title }}</strong> (User ID: {{ incident.user_id }})
          <p>{{ incident.description }}</p>
        </div>
        <div class="incident-actions">
          <select v-model="incident.status" @change="handleUpdateIncident(incident)">
            <option v-for="status in incidentStatusEnum" :value="status" :key="status">
              {{ status }}
            </option>
          </select>
          <button @click="handleDeleteIncident(incident.id)" class="delete-btn">Delete</button>
        </div>
      </li>
    </ul>
    <p v-if="!isLoading && !incidents.length">No incidents found.</p>
  </div>
</template>

<style scoped>
.incident-form {
  margin-bottom: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

ul {
  list-style: none;
  padding: 0;
}

li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem;
  border-bottom: 1px solid #eee;
}

.incident-details {
  flex-grow: 1;
}

.incident-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.delete-btn {
  background-color: #ff4d4d;
  color: white;
  border: none;
  padding: 0.3rem 0.6rem;
  border-radius: 4px;
  cursor: pointer;
}

.error {
  color: red;
  margin-bottom: 1rem;
}
</style>
