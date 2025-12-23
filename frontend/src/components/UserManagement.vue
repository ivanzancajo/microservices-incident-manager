<script setup>
import { ref, onMounted } from 'vue';
import { getUsers, createUser, deleteUser } from '../api';

const users = ref([]);
const newUser = ref({ name: '', email: '', password: '' });
const error = ref(null);
const isLoading = ref(true);
const successMessage = ref(null); // 1. NUEVO: Estado para el mensaje de éxito

const fetchUsers = async () => {
  try {
    isLoading.value = true;
    users.value = await getUsers();
    error.value = null;
  } catch (err) {
    error.value = `Error al cargar los usuarios: ${err.message}`;
  } finally {
    isLoading.value = false;
  }
};

const handleCreateUser = async () => {
  if (!newUser.value.name || !newUser.value.email || !newUser.value.password) {
    error.value = 'El nombre, el correo electrónico y la contraseña son obligatorios.';
    return;
  }
  try {
    await createUser({ ...newUser.value });
    newUser.value = { name: '', email: '', password: '' }; // Reset form
    await fetchUsers(); // Refresh list
  } catch (err) {
    error.value = `Error al crear el usuario: ${err.message}`;
  }
};

const handleDeleteUser = async (userId) => {
  // 1. IDENTIFICAR AL USUARIO ACTUAL
  // Recuperamos el email guardado en el login
  const loggedEmail = localStorage.getItem('user_email');
  
  // Buscamos en la lista de usuarios cargada (users.value) cuál coincide con mi email
  const currentUser = users.value.find(u => u.email === loggedEmail);
  const currentUserId = currentUser ? currentUser.id : null;

  // 2. DETECTAR SI ES AUTO-ELIMINACIÓN
  const isSelfDelete = (userId === currentUserId);

  // 3. CONFIGURAR EL AVISO
  let confirmMessage = "¿Estás seguro de que deseas eliminar este usuario?";

  if (isSelfDelete) {
    confirmMessage = "⚠️ AVISO IMPORTANTE ⚠️\n\nEstás a punto de eliminar tu cuenta de usuario.\n\nSi confirmas esta acción:\n1. Tu usuario será borrado permanentemente.\n2. Se cerrará tu sesión inmediatamente.\n3. Serás redirigido a la pantalla de Login.\n\n¿Deseas continuar?";
  }

  // 4. MOSTRAR CONFIRMACIÓN
  if (!confirm(confirmMessage)) {
    return; // El usuario canceló
  }

  try {
    // Llamada a la API para borrar
    await deleteUser(userId);

    // 5. ACCIONES POSTERIORES
    if (isSelfDelete) {
      // CASO A: Me borré a mí mismo -> Limpieza y Redirección
      localStorage.removeItem('token');
      localStorage.removeItem('user_email');
      localStorage.removeItem('refresh_token'); // Si lo usas
      
      // Forzamos la recarga de la página. 
      // Al no haber token, App.vue mostrará automáticamente el componente Login.
      window.location.reload(); 
    } else {
      // CASO B: Borré a otro -> Actualizar la lista (tu código original)
      await fetchUsers();
      error.value = null;
      successMessage.value = "Usuario eliminado correctamente.";
      
      setTimeout(() => {
        successMessage.value = null;
      }, 3000);
    }

  } catch (err) {
    successMessage.value = null;
    error.value = `Error al eliminar el usuario: ${err.message}`;
  }
};

onMounted(fetchUsers);
</script>

<template>
  <div class="user-management-container">
    <header>
      <h1>Gestión de Usuarios</h1>
    </header>

    <!-- Create User Form -->
    <form @submit.prevent="handleCreateUser" class="user-form">
      <h3>Añadir Nuevo Usuario</h3>
      <div class="form-group">
        <input type="text" v-model="newUser.name" placeholder="Nombre Completo" required />
      </div>
      <div class="form-group">
        <input type="email" v-model="newUser.email" placeholder="Correo Electrónico" required />
      </div>
      <div class="form-group">
        <input type="password" v-model="newUser.password" placeholder="Contraseña" required />
      </div>
      <button type="submit" class="btn-primary">Añadir Usuario</button>
    </form>

    <h2 class="list-title">Lista de Usuarios</h2>
    <div v-if="isLoading" class="loading">Cargando usuarios...</div>
    <div v-if="successMessage" class="success-message">
      <i class="fas fa-check-circle"></i> {{ successMessage }}
    </div>
    <div v-if="error" class="error">{{ error }}</div>

    <div class="user-list" v-if="!isLoading && users.length">
      <div v-for="user in users" :key="user.id" class="user-card">
        <div class="user-info">
          <strong class="user-name">{{ user.name }}</strong>
          <span class="user-email">{{ user.email }}</span>
        </div>
        <button @click="handleDeleteUser(user.id)" class="btn-danger">Eliminar</button>
      </div>
    </div>
    <p v-if="!isLoading && !users.length" class="no-users">No se encontraron usuarios. ¡Añade uno para empezar!</p>
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

.user-management-container {
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

.user-form {
  background-color: var(--card-background);
  padding: 2.5rem;
  border-radius: 12px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  margin-bottom: 2.5rem;
}

.user-form h3 {
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

input[type="text"],
input[type="email"],
input[type="password"] {
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

input[type="text"]:focus {
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
  /* width: 100%; removed */
  transition: all 0.3s ease;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
  text-transform: uppercase;
}

.btn-primary {
  background-color: rgb(250, 250, 250);
  color: #434190;
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

.user-list {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

.user-card {
  background-color: var(--card-background);
  border-radius: 12px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  transition: transform 0.3s, box-shadow 0.3s;
}

.user-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

.user-info {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-weight: 500;
  font-size: 1.1rem;
}

.user-email {
  color: var(--dark-gray);
  font-size: 0.9rem;
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

.loading, .no-users, .error {
  text-align: center;
  padding: 3rem;
  font-size: 1.2rem;
  color: var(--dark-gray);
}

.success-message {
  text-align: center;
  padding: 1rem;
  margin-bottom: 1rem;
  font-size: 1rem;
  color: #22543d;             /* Texto verde oscuro */
  background-color: #c6f6d5;  /* Fondo verde claro */
  border: 1px solid #22543d;
  border-radius: 8px;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
}

.error {
  color: var(--danger-color);
  background-color: #fed7d7;
  border: 1px solid var(--danger-color);
  border-radius: 8px;
}
</style>
