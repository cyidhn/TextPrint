<template>
  <v-card height="97vh">
    <v-navigation-drawer absolute permanent left width="100%">
      <template v-slot:prepend>
        <v-list-item two-line>
          <h1 class="blue--text text--darken-4">TEXT|<b>PRINT</b></h1>
        </v-list-item>
      </template>

      <v-divider></v-divider>

      <v-list dense>
        <v-list-item
          v-for="item in items"
          :key="item.title"
          @click="eventClick(item.link)"
        >
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title v-html="item.title"></v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
  </v-card>
</template>

<script>
import { TabsData } from "../flux/Tabs";

export default {
  data: () => ({
    principal: [
      { title: "Fichier", icon: "mdi-file", link: "fichier" },
      { title: "Nouveau", icon: "mdi-pencil", link: "nouveau" },
      { title: "Analyses", icon: "mdi-file-find", link: "analyses" },
      { title: "Rapports", icon: "mdi-library-books", link: "rapports" },
      { title: "Bases de données", icon: "mdi-database", link: "database" },
      { title: "Paramètres", icon: "mdi-settings", link: "params" }
    ],
    fichier: [
      {
        title: "<b>Retour</b>",
        icon: "mdi-keyboard-backspace",
        link: "retour"
      },
      { title: "Ouvrir", icon: "mdi-file", link: "ouvrir" },
      { title: "Importer", icon: "mdi-pencil", link: "importer" }
    ],
    nouveau: [
      {
        title: "<b>Retour</b>",
        icon: "mdi-keyboard-backspace",
        link: "retour"
      },
      { title: "Profil connu", icon: "mdi-account", link: "ouvrir" },
      { title: "Profil anonyme", icon: "mdi-account", link: "ouvrir" },
      { title: "Texte", icon: "mdi-file", link: "ouvrir" },
      { title: "Dossier", icon: "mdi-folder", link: "ouvrir" },
      {
        title: "Collection",
        icon: "mdi-folder-multiple",
        link: "ouvrir"
      }
    ],
    items: []
  }),
  mounted: function() {
    this.items = [...this.principal];
  },
  methods: {
    hello() {
      console.log("Hello");
    },
    back() {
      this.principal = true;
    },
    eventClick(ref) {
      if (ref === "retour") {
        this.items = this.principal;
      }
      if (ref === "fichier") {
        this.items = this.fichier;
      }
      if (ref === "nouveau") {
        this.items = this.nouveau;
      }
      if (ref === "database") {
        TabsData.bdd();
      }
    }
  }
};
</script>
