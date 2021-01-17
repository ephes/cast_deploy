<template>
  <h1>Home Page</h1>
  <p>Message from api:</p>
  {{ message }}
</template>
<script>
import { ref } from 'vue';

export default {
  name: 'Home',
  props: {
    user: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const message = ref('');
    const getMessageFromApi = async (client) => {
      client.get('http://localhost:8000/hello').then((response) => {
        console.log(response);
        message.value = response.data.message;
      });
    };

    return {
      message,
      getMessageFromApi,
    };
  },

  mounted() {
    console.log('home mounted..');
    this.getMessageFromApi(this.axios);
  },
};
</script>