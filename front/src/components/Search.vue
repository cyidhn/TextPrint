<template>
  <div>
    <div v-if="getError">
      <p>Impossible de charger les données. Une erreur s'est produite</p>
    </div>
    <div v-else>
      <v-card class="mx-auto" max-width="1200" tile>
        <v-text-field v-model="recherche" label="Rechercher dans la base de données" required></v-text-field>
        <v-list>
          <v-list-item-group color="primary">
            <v-list-item v-for="(item, i) in filteredList" :key="i" @click="addWindow(item)">
              <v-list-item-icon>
                <div v-if="item.type === 'Texte'">
                  <v-icon v-text="text"></v-icon>
                </div>
                <div v-if="item.type === 'Dossiers'">
                  <v-icon v-text="dossiers"></v-icon>
                </div>
                <div v-if="item.type === 'Collections'">
                  <v-icon v-text="collection"></v-icon>
                </div>
                <div v-if="item.type === 'Profil'">
                  <v-icon v-text="profil"></v-icon>
                </div>
              </v-list-item-icon>
              <v-list-item-content>
                Type : {{ item.type }} | Identifiant :
                {{ item.titre ? item.titre : item.alias }}
                {{ item.alias === "" ? item.prenom + " " + item.nom : "" }}
              </v-list-item-content>
            </v-list-item>
          </v-list-item-group>
        </v-list>
      </v-card>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { TabsData } from "../flux/Tabs";
// import { DialogsData } from "../flux/Dialogs";

export default {
  data: () => ({
    recherche: "",
    content: [],
    getError: false,
    logo: "mdi-account",
    file: "mdi-file",
    text: "mdi-message-text",
    profil: "mdi-account",
    collection: "mdi-folder-multiple",
    dossiers: "mdi-folder"
  }),
  mounted: function() {
    axios
      .get(process.env.VUE_APP_SERVEUR + "/test")
      .then(response => {
        this.content = response.data;
      })
      .catch(e => {
        this.getError = true;
        console.error("Impossible de charger les données", e);
      });
  },
  methods: {
    addWindow(item) {
      if (item.titre === undefined) {
        if (item.alias === undefined) {
          let nom = item.prenom + " " + item.nom;
          TabsData.add(nom, item);
        } else {
          TabsData.add(item.alias, item);
        }
      } else {
        TabsData.add(item.titre, item);
      }
    },
    updateContent() {
      axios
        .get(process.env.VUE_APP_SERVEUR + "/test")
        .then(response => {
          this.content = response.data;
        })
        .catch(e => {
          this.getError = true;
          console.error("Impossible de charger les données", e);
        });
    }
  },
  computed: {
    filteredList() {
      return this.content.filter(p => {
        try {
          return p.titre.toLowerCase().includes(this.recherche.toLowerCase());
        } catch {
          return p.alias.toLowerCase().includes(this.recherche.toLowerCase());
        }
      });
    }
  }
};
</script>
