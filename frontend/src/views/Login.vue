<template>
  <h1>Login View</h1>
  <p>Logged In state: {{ state.isAuthenticated }}</p>
  <button @click="login">
    Log in..
  </button>
</template>
<script>
import { reactive } from "vue";
import { useRouter } from 'vue-router'

import api from "../api"

export default {
  name: 'Home',
  setup() {
    const router = useRouter()

    function login() {
      api.isAuthenticated = true;
      router.push('/')
    }

    return {
      state: {
        isAuthenticated: api.isAuthenticated,
      },
      login: login,
    };
  },
};
</script>