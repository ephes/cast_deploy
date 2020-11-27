<template>
  <h1>{{ msg }}</h1>
  <button @click="count++">count is: {{ count + 1 }}</button>
  <p>
    Edit <code>components/HelloWorld.vue</code> to test hot module replacement.
  </p>
</template>

<script>
import axios from 'axios'

export default {
  name: 'DeploymentList',
  props: {
    msg: String,
  },
  data() {
    return {
      count: 0,
    };
  },
  mounted() {
    console.log('deployment list mounted..');
    axios
      .get('http://localhost:8000/hello')
      .then((response) => console.log(response));
  },
};
</script>
