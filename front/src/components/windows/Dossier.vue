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
          <v-text-field class="mx-2" v-model="search" label="Filtrer" single-line hide-details></v-text-field>
        </v-col>
      </v-row>
      <br />
      <v-data-table
        v-model="selected"
        :headers="headers"
        :items="desserts"
        :search="search"
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
          <v-text-field class="mx-2" v-model="search1" label="Filtrer" single-line hide-details></v-text-field>
        </v-col>
      </v-row>
      <br />
      <v-data-table
        v-model="selected"
        :headers="headers"
        :items="desserts"
        :search="search1"
        item-key="id"
        show-select
        class="elevation-1"
      ></v-data-table>
    </v-container>
  </div>
</template>

<script>
export default {
  data() {
    return {
      search: "",
      search1: "",
      selected: [],
      headers: [
        {
          text: "Type",
          value: "name"
        },
        { text: "Alias", value: "calories" },
        { text: "Prénom NOM", value: "fat" }
      ],
      desserts: [
        {
          id: 1,
          name: "Profil connu",
          calories: "Jane_Doe",
          fat: "Jane DOE"
        },
        {
          id: 2,
          name: "Profil anonyme",
          calories: "J_Dupond_123",
          fat: "/"
        },
        {
          id: 3,
          name: "Profil connu",
          calories: "/",
          fat: "Léo MARTIN"
        }
      ]
    };
  }
};
</script>
