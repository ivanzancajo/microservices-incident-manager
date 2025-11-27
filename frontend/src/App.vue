<script setup>
import { ref } from 'vue';
import UserManagement from './components/UserManagement.vue';
import IncidentManagement from './components/IncidentManagement.vue';

const currentView = ref('users'); // 'users' or 'incidents'
</script>

<template>
  <div class="app-container">
    <header class="app-header">
      <h1 class="app-title">Gestor de Usuarios e Incidencias</h1>
      <nav class="app-nav">
        <button @click="currentView = 'users'" :class="['nav-button', { active: currentView === 'users' }]">
          <i class="fas fa-users"></i> Usuarios
        </button>
        <button @click="currentView = 'incidents'" :class="['nav-button', { active: currentView === 'incidents' }]">
          <i class="fas fa-exclamation-triangle"></i> Incidencias
        </button>
      </nav>
    </header>

    <main class="app-main">
      <transition name="fade" mode="out-in">
        <component :is="currentView === 'users' ? UserManagement : IncidentManagement" />
      </transition>
    </main>
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

.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2.5rem;
  background-color: var(--card-background);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  z-index: 10;
}

.app-title {
  color: var(--primary-hover-color);
  font-size: 1.75rem;
  font-weight: 600;
}

.app-nav {
  display: flex;
  gap: 1rem;
}

.nav-button {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background-color: transparent;
  border: 2px solid transparent;
  color: var(--dark-gray);
  padding: 0.75rem 1.25rem;
  font-size: 1rem;
  font-weight: 500;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
}

.nav-button:hover {
  color: var(--primary-color);
  background-color: #eef2ff;
}

.nav-button.active {
  color: var(--primary-color);
  background-color: #eef2ff;
  border-color: var(--primary-color);
}

.nav-button .fas {
  font-size: 1.1em;
}

.app-main {
  flex: 1;
  padding: 2rem;
}

/* Transition effects */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
