<template>
    <div>
        <div class="background">
        <div class="shape"></div>
        <div class="shape"></div>
    </div>
    <form @submit.prevent="handleLogin" class="form-login">
      <h3>Login Here</h3>
      <label for="username" class="label-login">Username</label>
      <input type="text" v-model="username" placeholder="Email" id="username" class="input-login" required>
      <label for="password" class="label-login">Password</label>
      <input type="password" v-model="password" placeholder="Password" id="password" class="input-login" required>
      <button type="submit" class="btn-login">Log In</button>
      <div class="social"></div>
    </form>
    </div>
</template>


<script setup lang="ts">
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/authStore'; 

const username = ref<string>('');
const password = ref<string>('');
const router = useRouter();
const authStore = useAuthStore(); 

const handleLogin = async () => {
  try {
    const response = await axios.post('http://localhost:8000/login', new URLSearchParams({
      username: username.value,
      password: password.value
    }), {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });
    
    authStore.login(response.data.role);
    router.push('/inputForm');
  } catch (error) {
    console.error("Login failed: ", error);
    alert("Login failed. Please check your credentials.");
  }
};
</script>