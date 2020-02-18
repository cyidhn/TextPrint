<template>
  <v-container fluid>
    <br /><br />
    <v-row>
      <v-col cols="6" align="start">
        <h2>Association avec les Profils</h2>
      </v-col>
      <v-col cols="6" align="end">
        <v-btn small class="mx-2" color="primary">Ajouter un profil</v-btn>
        <v-btn small color="error">Supprimer la sélection</v-btn>
      </v-col>
    </v-row>
    <br />
    <v-data-table
      v-model="selected"
      :headers="headers"
      :items="desserts"
      item-key="name"
      show-select
      class="elevation-1"
    >
    </v-data-table>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      selected: [],
      headers: [
        {
          text: "Type",
          align: "left",
          value: "name"
        },
        { text: "Alias", value: "calories" },
        { text: "Prénom NOM", value: "fat" }
      ],
      desserts: [
        {
          name: "Profil connu",
          calories: "Jane_Doe",
          fat: "Jane DOE"
        },
        {
          name: "Profil anonyme",
          calories: "J_Dupond_123",
          fat: "/"
        },
        {
          name: "Profil connu",
          calories: "/",
          fat: "Léo MARTIN"
        }
      ]
    };
  }
};
</script>
