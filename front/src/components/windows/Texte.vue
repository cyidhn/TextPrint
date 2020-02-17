<template>
  <div>
    <v-form ref="form">
      <v-row align="start" justify="start">
        <v-col cols="12">
          <h2>Identification</h2>
        </v-col>
        <v-col cols="12" sm="6" md="4">
          <v-text-field
            v-model="titre"
            label="Titre*"
            autocomplete="nope"
            hint="Titre du fichier"
            required
          ></v-text-field>
        </v-col>
        <v-col cols="12" sm="6" md="4">
          <v-text-field
            v-model="paternite"
            label="Paternité*"
            autocomplete="nope"
            hint="Paternité du texte"
            required
          ></v-text-field>
        </v-col>
      </v-row>
    </v-form>
  </div>
</template>

<script>
export default {
  props: {
    content: Object
  },
  data: () => ({
    titre: "",
    paternite: ""
  }),
  mounted() {
    console.log(this.content);
    this.titre = this.content.titre;
    this.paternite = this.content.paternite;
  }
};
</script>
