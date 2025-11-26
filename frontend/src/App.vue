<script setup>
import UserManagement from './components/UserManagement.vue';
import IncidentManagement from './components/IncidentManagement.vue';
</script>

<template>
  <header>
    <h1>Incidents & Users Management</h1>
  </header>

  <main>
    <section class="management-section">
      <UserManagement />
    </section>
    <section class="management-section">
      <IncidentManagement />
    </section>
  </main>
</template>

<style scoped>
header {
  background-color: #f0f0f0;
  padding: 1rem;
  text-align: center;
}

main {
  display: flex;
  justify-content: space-around;
  padding: 1rem;
}

.management-section {
  width: 48%;
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 1rem;
}
</style>
