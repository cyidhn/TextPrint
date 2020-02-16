<template>
  <div>
    <p>Search content</p>
    <div v-if="getError">
      <p>Impossible de charger les données. Une erreur s'est produite</p>
    </div>
    <div v-else>
      <p>Chagement des données</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data: () => ({
    content: [],
    getError: false
  }),
  mounted: function() {
    axios
      .get("https://jsonplaceholder.typicode.com/posts")
      .then(response => {
        this.content = response.data;
      })
      .catch(e => {
        this.getError = true;
        console.error("Impossible de charger les données", e);
      });
  }
};
</script>
