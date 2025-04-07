<template>
  <div class="app-container">
    <header class="app-header">
      <img src="./assets/img/logo.jpeg" alt="Logo" class="logo" />
      <div v-if="isAuthenticated" class="logout-button">
        <button @click="handleLogout">Logout</button>
      </div>
    </header>
    <UApp>
      <NuxtPage />
    </UApp>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useAuthStore } from '@/stores/authStore'; 
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();

const isAuthenticated = computed(() => authStore.isAuthenticated);

const handleLogout = () => {
  authStore.logout(); 
  router.push('/'); 
};
</script>


