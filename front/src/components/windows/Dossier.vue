<template>
  <div>
    <v-container fluid>
      <br />
      <br />
      <v-row>
        <v-col cols="6" align="start">
          <h2>Association avec les Profils</h2>
        </v-col>
        <v-col cols="6" align="end">
          <v-btn small class="mx-2" color="primary">Ajouter un profil</v-btn>
          <v-btn
            small
            color="error"
            :disabled="disabledProfils"
            @click="deleteProfils"
          >Supprimer la sélection</v-btn>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="6" align="start">
          <v-text-field
            class="mx-2"
            v-model="searchProfils"
            label="Filtrer"
            single-line
            hide-details
          ></v-text-field>
        </v-col>
      </v-row>
      <br />
      <v-data-table
        no-data-text="Aucu
        n élément trouvé"
        no-results-text="Aucun élément trouvé"
        loading-text="Chargement en cours..."
        v-model="selectedProfils"
        :headers="headersProfils"
        :items="profils"
        :search="searchProfils"
        item-key="id"
        show-select
        class="elevation-1"
      ></v-data-table>
    </v-container>
    <v-container fluid>
      <br />
      <br />
      <v-row>
        <v-col cols="6" align="start">
          <h2>Association avec les Textes</h2>
        </v-col>
        <v-col cols="6" align="end">
          <v-btn small class="mx-2" color="primary">Ajouter un texte</v-btn>
          <v-btn small color="error" :disabled="disabledTextes">Supprimer la sélection</v-btn>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="6" align="start">
          <v-text-field
            class="mx-2"
            v-model="searchTextes"
            label="Filtrer"
            single-line
            hide-details
          ></v-text-field>
        </v-col>
      </v-row>
      <br />
      <v-data-table
        no-data-text="Aucun élément trouvé"
        no-results-text="Aucun élément trouvé"
        loading-text="Chargement en cours..."
        v-model="selectedTextes"
        :headers="headersTextes"
        :items="textes"
        :search="searchTextes"
        item-key="id"
        show-select
        class="elevation-1"
      ></v-data-table>
    </v-container>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      disabledProfils: true,
      disabledTextes: true,
      searchProfils: "",
      searchTextes: "",
      selectedProfils: [],
      selectedTextes: [],
      headersProfils: [
        { text: "Type", value: "type" },
        { text: "Alias", value: "alias" },
        { text: "Prénom NOM", value: "nom" }
      ],
      profils: [],
      headersTextes: [
        { text: "Titre", value: "titre" },
        { text: "# Versions", value: "version" }
      ],
      textes: []
    };
  },
  methods: {
    deleteProfils() {
      if (confirm("Voulez-vous vraiment supprimer cette association ?")) {
        let formData = new FormData();
        this.selectedProfils.map(e => {
          formData = new FormData();
          formData.append("id", e.delete);
          // Appel avec axios
          axios
            .post(
              process.env.VUE_APP_SERVEUR + "/supprimer-association",
              formData
            )
            .then(response => {
              console.log(response.data);
              // Supprimer du tableau
              for (var i = 0; i < this.profils.length; i++) {
                if (this.profils[i].delete === e.delete) {
                  this.profils.splice(i, 1);
                }
              }
            })
            .catch(error => {
              console.log(error);
            });
        });
        this.selectedProfils = [];
      }
    }
  },
  mounted: function() {
    // TypeProfils
    // Ajout en formulaire
    let formData = new FormData();
    formData.append("id", 2);
    formData.append("type", "Dossier");
    formData.append("get", "Profil");

    // Appel avec axios
    axios
      .post(process.env.VUE_APP_SERVEUR + "/assoc", formData)
      .then(response => {
        let result = JSON.parse(response.data);
        this.profils = result;
      })
      .catch(error => {
        console.log(error);
      });
    // /TypeProfils

    // TypeTextes
    // Ajout en formulaire
    formData = new FormData();
    formData.append("id", 2);
    formData.append("type", "Dossier");
    formData.append("get", "Texte");

    // Appel avec axios
    axios
      .post(process.env.VUE_APP_SERVEUR + "/assoc", formData)
      .then(response => {
        let result = JSON.parse(response.data);
        this.textes = result;
      })
      .catch(error => {
        console.log(error);
      });
    // /TypeTextes
  },
  updated: function() {
    // Profils
    if (this.selectedProfils.length > 0) {
      this.disabledProfils = false;
    } else {
      this.disabledProfils = true;
    }
    // Textes
    if (this.selectedTextes.length > 0) {
      this.disabledTextes = false;
    } else {
      this.disabledTextes = true;
    }
  }
};
</script>
