<script setup>
import { ref } from 'vue';
import UserManagement from './components/UserManagement.vue';
import IncidentManagement from './components/IncidentManagement.vue';

const currentView = ref('users'); // 'users' or 'incidents'
</script>

<template>
  <header>
    <h1>Gestor de usuarios e incidencias</h1>
    <nav>
      <button @click="currentView = 'users'" :class="{ active: currentView === 'users' }">
        Usuarios
      </button>
      <button @click="currentView = 'incidents'" :class="{ active: currentView === 'incidents' }">
        Incidencias
      </button>
    </nav>
  </header>

  <main>
    <section class="management-section">
      <UserManagement v-if="currentView === 'users'" />
      <IncidentManagement v-else />
    </section>
  </main>
</template>

<style scoped>
header {
  background-color: #fff;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 2rem;
  position: sticky;
  top: 0;
  z-index: 1000;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  border-radius: 8px;
  margin: 0.5rem;
  height: 4rem;
}

h1 {
  color: #434190;
  font-size: 1.5rem;
}

nav button {
  background: none;
  border: none;
  padding: 0;
  margin-left: 1.5rem;
  font-size: 1.5rem;
  font-family: inherit;
  cursor: pointer;
  transition: color 0.3s ease-in-out;
}

nav button:hover {
  color: #434190;
}

nav button.active {
  color: #434190;
  font-weight: bold;
}

main {
  padding: 1rem;
  margin-top: 1rem;
  display: flex;
  justify-content: center;
}

.management-section {
  width: 96%;
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 1rem;
}
</style>
