<script setup>
import { ref, onMounted } from 'vue';
import UserManagement from './components/UserManagement.vue';
import IncidentManagement from './components/IncidentManagement.vue';
import Login from './components/Login.vue';

// Estado para controlar qué vista mostramos (Usuarios o Incidencias)
const currentView = ref('users'); 

// Estado para saber si el usuario está logueado
const isAuthenticated = ref(false);

// Al arrancar, comprobamos si ya hay un token guardado
onMounted(() => {
  const token = localStorage.getItem('token');
  if (token) {
    isAuthenticated.value = true;
  }
});

// Función que se ejecuta cuando el componente Login nos avisa de que todo fue bien
const handleLoginSuccess = () => {
  isAuthenticated.value = true;
  currentView.value = 'incidents'; // Redirigimos a incidencias por defecto al entrar
};

// Función para cerrar sesión
const handleLogout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('user_email');
  isAuthenticated.value = false;
  currentView.value = 'users'; // Reset de la vista
};
</script>

<template>
  <div class="app-container">
    
    <transition name="fade" mode="out-in">
      <Login 
        v-if="!isAuthenticated" 
        @login-success="handleLoginSuccess" 
      />

      <div v-else class="authenticated-layout">
        <header class="app-header">
          <div class="header-content">
            <h1 class="app-title">Gestor de Incidencias</h1>
            
            <nav class="app-nav">
              <button 
                @click="currentView = 'users'" 
                :class="['nav-button', { active: currentView === 'users' }]"
              >
                <i class="fas fa-users"></i> Usuarios
              </button>
              <button 
                @click="currentView = 'incidents'" 
                :class="['nav-button', { active: currentView === 'incidents' }]"
              >
                <i class="fas fa-exclamation-triangle"></i> Incidencias
              </button>
              
              <div class="separator"></div>

              <button @click="handleLogout" class="nav-button logout-btn">
                <i class="fas fa-sign-out-alt"></i> Salir
              </button>
            </nav>
          </div>
        </header>

        <main class="app-main">
          <transition name="fade" mode="out-in">
            <component :is="currentView === 'users' ? UserManagement : IncidentManagement" />
          </transition>
        </main>
      </div>
    </transition>

  </div>
</template>

<style>
/* Global Styles */
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap');

:root {
  --primary-color: #5a67d8;
  --primary-hover-color: #434190;
  --danger-color: #e53e3e;
  --danger-hover-color: #c53030;
  --background-color: #f7fafc;
  --card-background: #ffffff;
  --text-color: #2d3748;
  --light-gray: #e2e8f0;
  --dark-gray: #718096;
}

body {
  font-family: 'Poppins', sans-serif;
  background-color: var(--background-color);
  color: var(--text-color);
  margin: 0;
}

/* App Layout */
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.authenticated-layout {
  display: flex;
  flex-direction: column;
  width: 100%;
  min-height: 100vh;
}

.app-header {
  background-color: var(--card-background);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  z-index: 10;
  position: sticky;
  top: 0;
  width: 100%;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2.5rem;
  max-width: 1200px;
  margin: 0 auto;
}

.app-title {
  color: var(--primary-hover-color);
  font-size: 1.5rem; /* Un poco más pequeño para encajar mejor */
  font-weight: 600;
  margin: 0;
}

.app-nav {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.nav-button {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background-color: transparent;
  border: 2px solid transparent;
  color: var(--dark-gray);
  padding: 0.5rem 1rem;
  font-size: 0.95rem;
  font-weight: 500;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
}

.nav-button:hover {
  color: var(--primary-color);
  background-color: #eef2ff;
}

.nav-button.active {
  color: var(--primary-color);
  background-color: #eef2ff;
  border-color: #eef2ff; /* Sutil borde para indicar activo */
}

/* Estilos específicos para el botón de Salir */
.logout-btn {
  color: var(--danger-color);
  border: 1px solid var(--light-gray);
}

.logout-btn:hover {
  background-color: #fff5f5;
  color: var(--danger-hover-color);
  border-color: var(--danger-color);
}

.separator {
  width: 1px;
  height: 24px;
  background-color: var(--light-gray);
  margin: 0 0.5rem;
}

.app-main {
  flex: 1;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  box-sizing: border-box;
}

/* Transition effects */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>