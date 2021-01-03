<template>
  <h1>Home Page</h1>
  <p>Message from api:</p>
  {{ state.message }}
</template>
<script>
import { reactive } from "vue";

export default {
  name: 'Home',
  setup() {
    const state = reactive({
      message: "no message yet..",
    });

    return {
      state,
    };
  },

  mounted() {
    console.log("home mounted..");
    this.axios
      .get("http://localhost:8000/hello")
      .then((response) => {
        console.log(response)
        this.state.message = response.data.message;
      });
  },
};
</script>