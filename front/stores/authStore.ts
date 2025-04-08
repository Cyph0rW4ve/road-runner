import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useAuthStore = defineStore('auth', () => {
  const isAuthenticated = ref<boolean>(false);
  const userRole = ref<string | null>(null);

  function login(role: string) {
    isAuthenticated.value = true;
    userRole.value = role;
  }

  function logout() {
    isAuthenticated.value = false;
    userRole.value = null;
  }

  return { isAuthenticated, userRole, login, logout };
});