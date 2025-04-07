import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/stores/authStore'; 
import InputForm from '@/pages/inputForm.vue';
import Index from '@/pages/index.vue';

const routes = [
  { path: '/', component: Index },
  { path: '/inputForm', component: InputForm, meta: { requiresAuth: true } },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  if (to.matched.some(record => record.meta.requiresAuth) && !authStore.isAuthenticated) {
    next('/');
  } else {
    next();
  }
});

export default router;