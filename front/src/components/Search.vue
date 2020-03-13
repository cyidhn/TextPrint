<template>
  <div>
    <div v-if="getError">
      <p>Impossible de charger les données. Une erreur s'est produite</p>
    </div>
    <div v-else>
      <v-card class="mx-auto" max-width="1200" tile>
        <v-row justify="space-around">
          <v-col cols="12">
            <v-text-field
              v-model="recherche"
              label="Rechercher dans la base de données"
              required
              @click="updateContent"
            ></v-text-field>
          </v-col>
          <v-switch
            v-model="filterTextes"
            class="ma-2"
            label="Textes"
            @change="updateContent()"
          ></v-switch>
          <v-switch
            v-model="filterDossiers"
            class="ma-2"
            label="Dossiers"
            @change="updateContent()"
          ></v-switch>
          <v-switch
            v-model="filterCollections"
            class="ma-2"
            label="Collections"
            @change="updateContent()"
          ></v-switch>
          <v-switch
            v-model="filterProfils"
            class="ma-2"
            label="Profil"
            @change="updateContent()"
          ></v-switch>
        </v-row>
        <v-list>
          <hr />
          <v-list-item-group color="primary">
            <v-list-item
              v-for="(item, i) in filteredList"
              :key="i"
              @click="addWindow(item)"
            >
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
    // Filtres
    filterTextes: true,
    filterDossiers: true,
    filterCollections: true,
    filterProfils: true,
    // Courbes
    labels: ["12am", "3am", "6am", "9am", "12pm", "3pm", "6pm", "9pm"],
    value: [200, 675, 410, 390, 310, 460, 250, 240],
    // Autre
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
        this.content = this.shuffleContent(this.content);
      })
      .catch(e => {
        this.getError = true;
        console.error("Impossible de charger les données", e);
      });
  },
  methods: {
    shuffleContent(a) {
      var j, x, i;
      for (i = a.length - 1; i > 0; i--) {
        j = Math.floor(Math.random() * (i + 1));
        x = a[i];
        a[i] = a[j];
        a[j] = x;
      }
      return a;
    },
    updateSelection() {
      // Mettre à jour les contenus
      // Filtrer un texte
      if (!this.filterTextes) {
        // False
        for (let i = 0; i < this.content.length; i++) {
          if (this.content[i].type == "Texte") {
            this.content.splice(i, 1);
            i--;
          }
        }
      }

      // Filtrer un dossier
      if (!this.filterDossiers) {
        // False
        for (let i = 0; i < this.content.length; i++) {
          if (this.content[i].type == "Dossiers") {
            this.content.splice(i, 1);
            i--;
          }
        }
      }

      // Filtrer une collection
      if (!this.filterCollections) {
        // False
        for (let i = 0; i < this.content.length; i++) {
          if (this.content[i].type == "Collections") {
            this.content.splice(i, 1);
            i--;
          }
        }
      }

      // Filtrer un profil
      if (!this.filterProfils) {
        // False
        for (let i = 0; i < this.content.length; i++) {
          if (this.content[i].type == "Profil") {
            this.content.splice(i, 1);
            i--;
          }
        }
      }
    },
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
          this.content = this.shuffleContent(this.content);
          this.updateSelection();
        })
        .catch(e => {
          this.getError = true;
          console.error("Impossible de charger les données", e);
        });
    }
  },
  computed: {
    keywords() {
      if (!this.filteredList) return [];

      const keywords = [];

      for (const search of this.filteredList) {
        if (!keywords.includes(search.type)) {
          keywords.push(search.type);
        }
      }

      return keywords;
    },
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
