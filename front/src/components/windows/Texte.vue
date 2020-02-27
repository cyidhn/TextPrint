<template>
  <div>
    <v-container>
      <v-row class="mt-8">
        <v-col cols="6" align="start">
          <h3 class="mb-4">Texte original</h3>
          <iframe class="border-iframe" width="100%" height="500" :src="link"></iframe>
        </v-col>
        <v-col cols="6" align="start">
          <h3 class="mb-4">Premières analyses</h3>
          <iframe class="border-iframe" width="100%" height="500" :src="linkAnalyse"></iframe>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
export default {
  props: {
    content: Object
  },
  data: () => ({
    titre: "",
    paternite: "",
    linkAnalyse: "",
    link: ""
  }),
  mounted() {
    console.log(this.content);
    this.titre = this.content.titre;
    this.paternite = this.content.paternite;
    this.link =
      process.env.VUE_APP_SERVEUR +
      "/static/textes/" +
      this.content.fichier +
      ".txt";

    this.linkAnalyse =
      process.env.VUE_APP_SERVEUR +
      "/static/textes/" +
      this.content.fichier +
      "_analyse.html";
  }
};
</script>

<style scoped>
.border-iframe {
  border: 1px black solid;
}
</style>
