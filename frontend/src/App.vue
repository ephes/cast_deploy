<template>
  <div id="app">
    <div v-if="state.loggedIn" id="nav">
      <router-link to="/">Home</router-link> |
      <router-link to="/about">About</router-link>
    </div>
    <router-view />
  </div>
</template>
<script>
import { reactive, computed } from "vue";
import api from './api'

export default {
  name: 'App',
  setup() {
    const state = {
      loggedIn: api.isAuthenticated
    }

    return {
      state,
    };
  },
  mounted() {
    console.log('app mounted')
    console.log('is authenticated: ', api.isAuthenticated)
    if (!api.isAuthenticated) {
      this.$router.push('/login')
    }
  }
};
</script>