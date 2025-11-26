<script setup>
import { ref, onMounted } from 'vue';
import { getUsers, createUser, deleteUser } from '../api';

const users = ref([]);
const newUser = ref({ name: '', email: '' });
const error = ref(null);
const isLoading = ref(true);

const fetchUsers = async () => {
  try {
    isLoading.value = true;
    users.value = await getUsers();
    error.value = null;
  } catch (err) {
    error.value = `Error loading users: ${err.message}`;
  } finally {
    isLoading.value = false;
  }
};

const handleCreateUser = async () => {
  if (!newUser.value.name || !newUser.value.email) {
    error.value = 'Name and email are required.';
    return;
  }
  try {
    await createUser({ ...newUser.value });
    newUser.value = { name: '', email: '' }; // Reset form
    await fetchUsers(); // Refresh list
  } catch (err) {
    error.value = `Error creating user: ${err.message}`;
  }
};

const handleDeleteUser = async (userId) => {
  try {
    await deleteUser(userId);
    await fetchUsers(); // Refresh list
  } catch (err) {
    error.value = `Error deleting user: ${err.message}`;
  }
};

onMounted(fetchUsers);
</script>

<template>
  <div>
    <h2>User Management</h2>
    
    <!-- Create User Form -->
    <form @submit.prevent="handleCreateUser" class="user-form">
      <input type="text" v-model="newUser.name" placeholder="Name" required />
      <input type="email" v-model="newUser.email" placeholder="Email" required />
      <button type="submit">Create User</button>
    </form>

    <!-- Loading and Error Messages -->
    <div v-if="isLoading">Loading users...</div>
    <div v-if="error" class="error">{{ error }}</div>

    <!-- Users List -->
    <ul v-if="!isLoading && users.length">
      <li v-for="user in users" :key="user.id">
        <span>{{ user.name }} ({{ user.email }})</span>
        <button @click="handleDeleteUser(user.id)" class="delete-btn">Delete</button>
      </li>
    </ul>
    <p v-if="!isLoading && !users.length">No users found.</p>
  </div>
</template>

<style scoped>
.user-form {
  margin-bottom: 1rem;
  display: flex;
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
