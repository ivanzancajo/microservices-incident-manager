<script setup>
import { ref, onMounted } from 'vue';
import { getUsers, createUser, deleteUser } from '../api';

// --- ESTADO GENERAL ---
const users = ref([]);
const newUser = ref({ name: '', email: '', password: '' });
const error = ref(null);
const isLoading = ref(true);
const successMessage = ref(null);
// CORRECCIÓN: Guardamos el email en una variable reactiva para usarla en el template
const currentUserEmail = ref(localStorage.getItem('user_email') || '');

// --- ESTADO PARA EL MODAL PERSONALIZADO ---
const showDeleteModal = ref(false);
const userToDeleteId = ref(null);
const isSelfDelete = ref(false);
const isDeleting = ref(false);

// Cargar usuarios al inicio
const fetchUsers = async () => {
  try {
    isLoading.value = true;
    users.value = await getUsers();
    // Actualizamos el email actual por si ha cambiado
    currentUserEmail.value = localStorage.getItem('user_email');
    error.value = null;
  } catch (err) {
    error.value = `Error al cargar los usuarios: ${err.message}`;
  } finally {
    isLoading.value = false;
  }
};

// Crear usuario
const handleCreateUser = async () => {
  if (!newUser.value.name || !newUser.value.email || !newUser.value.password) {
    error.value = 'Todos los campos son obligatorios.';
    return;
  }
  try {
    await createUser({ ...newUser.value });
    newUser.value = { name: '', email: '', password: '' }; 
    await fetchUsers(); 
    showSuccess("Usuario creado correctamente");
  } catch (err) {
    error.value = `Error al crear el usuario: ${err.message}`;
  }
};

// --- LÓGICA DE BORRADO ---

// 1. Solicitud de borrado (Abre el modal)
const confirmDeleteRequest = (user) => {
  userToDeleteId.value = user.id;
  
  // Detectar si el usuario a borrar coincide con el logueado
  // Usamos la variable local, no localStorage directo
  isSelfDelete.value = (user.email === currentUserEmail.value);
  
  // Mostrar el modal
  showDeleteModal.value = true;
};

// 2. Ejecutar borrado (Al confirmar en el modal)
const executeDelete = async () => {
  if (!userToDeleteId.value) return;

  isDeleting.value = true; 

  try {
    await deleteUser(userToDeleteId.value);

    if (isSelfDelete.value) {
      // CASO A: El usuario se borró a sí mismo
      localStorage.removeItem('token');
      localStorage.removeItem('user_email');
      localStorage.removeItem('refresh_token');
      window.location.reload(); 
    } else {
      // CASO B: Borrado de otro usuario
      await fetchUsers();
      showSuccess("Usuario eliminado correctamente");
      closeModal();
    }
  } catch (err) {
    error.value = `Error al eliminar: ${err.message}`;
    closeModal();
  } finally {
    isDeleting.value = false;
  }
};

const closeModal = () => {
  showDeleteModal.value = false;
  userToDeleteId.value = null;
  isSelfDelete.value = false;
};

const showSuccess = (msg) => {
  successMessage.value = msg;
  setTimeout(() => {
    successMessage.value = null;
  }, 3000);
};

onMounted(fetchUsers);
</script>

<template>
  <div class="user-management-container">
    <header>
      <h1>Gestión de Usuarios</h1>
    </header>

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
          <span v-if="user.email === currentUserEmail" class="badge-me"> (Tú)</span>
        </div>
        <button @click="confirmDeleteRequest(user)" class="btn-danger">Eliminar</button>
      </div>
    </div>
    
    <p v-if="!isLoading && !users.length" class="no-users">No se encontraron usuarios. ¡Añade uno para empezar!</p>

    <div v-if="showDeleteModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-card" :class="{ 'modal-danger': isSelfDelete }">
        
        <div class="modal-icon">
          <i class="fas" :class="isSelfDelete ? 'fa-exclamation-triangle' : 'fa-trash-alt'"></i>
        </div>

        <h3 class="modal-title">
          {{ isSelfDelete ? '¿ELIMINAR TU CUENTA?' : '¿Eliminar usuario?' }}
        </h3>

        <div class="modal-body">
          <p v-if="!isSelfDelete">
            Esta acción no se puede deshacer. ¿Estás seguro de continuar?
          </p>
          <div v-else class="warning-box">
            <p><strong>⚠️ ADVERTENCIA CRÍTICA</strong></p>
            <ul>
              <li>Tu cuenta será borrada permanentemente.</li>
              <li>Se cerrará tu sesión actual.</li>
              <li>Serás redirigido al inicio de sesión.</li>
            </ul>
          </div>
        </div>

        <div class="modal-actions">
          <button @click="closeModal" class="btn-cancel" :disabled="isDeleting">Cancelar</button>
          <button @click="executeDelete" class="btn-confirm" :disabled="isDeleting">
            {{ isDeleting ? 'Borrando...' : (isSelfDelete ? 'Sí, eliminar mi cuenta' : 'Eliminar') }}
          </button>
        </div>
      </div>
    </div>

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
  background-color: white;
  -webkit-appearance: none; 
  appearance: none;
}

input:focus {
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

.badge-me {
  font-size: 0.8rem;
  color: var(--primary-color);
  font-weight: bold;
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
  color: #22543d;
  background-color: #c6f6d5;
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

/* --- ESTILOS DEL MODAL --- */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(3px);
  animation: fadeIn 0.2s ease-out;
}

.modal-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  width: 90%;
  max-width: 400px;
  text-align: center;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  animation: popIn 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.modal-danger {
  border-top: 5px solid var(--danger-color);
}

.modal-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  color: var(--dark-gray);
}

.modal-danger .modal-icon {
  color: var(--danger-color);
  animation: pulse 2s infinite;
}

.modal-title {
  margin: 0 0 1rem;
  font-size: 1.5rem;
  color: var(--text-color);
  font-weight: 600;
}

.modal-body {
  margin-bottom: 2rem;
  color: #4a5568;
}

.warning-box {
  background-color: #fff5f5;
  border: 1px solid #feb2b2;
  color: #c53030;
  padding: 1rem;
  border-radius: 8px;
  text-align: left;
  font-size: 0.9rem;
}

.warning-box ul {
  margin: 0.5rem 0 0 1.2rem;
  padding: 0;
}

.modal-actions {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
}

.btn-cancel, .btn-confirm {
  flex: 1;
  padding: 0.75rem;
  border-radius: 8px;
  border: none;
  font-weight: 600;
  cursor: pointer;
  font-size: 0.95rem;
  transition: opacity 0.2s;
}

.btn-cancel {
  background-color: #e2e8f0;
  color: #4a5568;
}

.btn-confirm {
  background-color: var(--danger-color);
  color: white;
}

.btn-cancel:hover, .btn-confirm:hover {
  opacity: 0.9;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes popIn {
  from { transform: scale(0.9); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
}
</style>