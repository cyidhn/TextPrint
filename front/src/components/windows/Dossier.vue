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
          <v-btn small color="error">Supprimer la sélection</v-btn>
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
        v-model="selected"
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
          <v-btn small color="error">Supprimer la sélection</v-btn>
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
        v-model="selected"
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
      searchProfils: "",
      searchTextes: "",
      selected: [],
      headersProfils: [
        { text: "Type", value: "type" },
        { text: "Alias", value: "alias" },
        { text: "Prénom NOM", value: "nom" }
      ],
      profils: [],
      headersTextes: [
        { text: "Titre", value: "titre" },
        { text: "# Versions", value: "versions" }
      ],
      textes: []
    };
  },
  mounted: function() {
    // Ajout en formulaire
    let formData = new FormData();
    formData.append("id", 2);
    formData.append("type", "Dossier");
    formData.append("get", "Profil");

    // Appel avec axios
    axios
      .post(process.env.VUE_APP_SERVEUR + "/assoc", formData)
      .then(response => {
        console.log(response.data);
        let result = JSON.parse(response.data);
        this.profils = [result];
      })
      .catch(error => {
        console.log(error);
      });
  }
};
</script>
