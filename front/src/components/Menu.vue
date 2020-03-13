<template>
  <v-card height="97vh">
    <v-navigation-drawer absolute permanent left width="100%">
      <template v-slot:prepend>
        <v-list-item two-line>
          <h1 class="blue--text text--darken-4">
            TEXT |
            <b>PRINT</b>
          </h1>
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
import { DialogsData } from "../flux/Dialogs";
import { ConnectData } from "../flux/Connect";

export default {
  data: () => ({
    principal: [
      { title: "Fichier", icon: "mdi-file", link: "fichier" },
      { title: "Nouveau", icon: "mdi-pencil", link: "nouveau" },
      { title: "Analyses", icon: "mdi-file-find", link: "analyses" },
      { title: "Rapports", icon: "mdi-folder-lock", link: "rapports" },
      { title: "Bases de données", icon: "mdi-database", link: "database" },
      { title: "Paramètres", icon: "mdi-message-alert", link: "params" }
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
    params: [
      {
        title: "<b>Retour</b>",
        icon: "mdi-keyboard-backspace",
        link: "retour"
      },
      { title: "Déconnexion", icon: "mdi-run", link: "deconnexion" }
    ],
    nouveau: [
      {
        title: "<b>Retour</b>",
        icon: "mdi-keyboard-backspace",
        link: "retour"
      },
      {
        title: "Profil connu",
        icon: "mdi-account-outline",
        link: "profil-connu"
      },
      { title: "Profil anonyme", icon: "mdi-account", link: "profil-anonyme" },
      { title: "Texte", icon: "mdi-file", link: "texte" },
      { title: "Dossier", icon: "mdi-folder", link: "dossier" },
      {
        title: "Collection",
        icon: "mdi-folder-multiple",
        link: "collection"
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
    setCookie(cname, cvalue, exdays) {
      var d = new Date();
      d.setTime(d.getTime() + exdays * 24 * 60 * 60 * 1000);
      var expires = "expires=" + d.toUTCString();
      document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
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
      if (ref === "params") {
        this.items = this.params;
      }
      if (ref === "database") {
        TabsData.bdd();
      }
      if (ref === "profil-connu") {
        DialogsData.open("profil-connu");
      }
      if (ref === "profil-anonyme") {
        DialogsData.open("profil-anonyme");
      }
      if (ref === "collection") {
        DialogsData.open("collection");
      }
      if (ref === "dossier") {
        DialogsData.open("dossier");
      }
      if (ref === "texte") {
        DialogsData.open("texte");
      }
      if (ref === "deconnexion") {
        this.setCookie("ctex", "1", 1);
        ConnectData.deconnexion();
      }
    }
  }
};
</script>
