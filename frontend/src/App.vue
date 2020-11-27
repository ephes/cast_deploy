<template>
  <img alt="Vue logo" src="./assets/logo.png" />
  <deployment-list msg="Hello Vue 3.0 + Vite" />
</template>

<script>
import DeploymentList from './components/DeploymentList.vue'

export default {
  name: 'App',
  components: {
    DeploymentList
  }
}
</script>
