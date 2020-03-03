<template>
  <div>
    <v-container>
      <v-row>
        <v-col cols="12">
          <v-btn
            @click="removeText"
            class="mr-3"
            depressed
            small
            color="primary"
          >Associer à des éléments</v-btn>
          <v-btn @click="removeText" depressed small color="error">Supprimer</v-btn>
        </v-col>
      </v-row>
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
import axios from "axios";
import { TabsData } from "../../flux/Tabs";

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
  methods: {
    removeText() {
      console.log(this.content.id);
      console.log(this.content);
      if (
        confirm(
          "Voulez-vous vraiment supprimer ce texte et ses analyses définitivement ?"
        )
      ) {
        // Appel avec axios
        let formData = new FormData();
        formData.append("id", this.content.id);
        axios
          .post(process.env.VUE_APP_SERVEUR + "/supprimer-texte", formData)
          .then(response => {
            alert("Le texte a bien été supprimé");
            TabsData.remove(TabsData.state.nowId);
            console.log(response);
          })
          .catch(error => {
            alert(error);
          });
      }
    }
  },
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
