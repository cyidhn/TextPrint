<template>
  <v-row justify="center">
    <button @click="checkDialog" v-if="!dialog">Hello</button>
    <v-dialog v-model="dialog" persistent scrollable max-width="500px">
      <v-card>
        <v-card-title>Créer un profil connu</v-card-title>
        <v-divider></v-divider>
        <v-card-text style="height: 300px;">
          <v-form ref="form" v-model="valid" lazy-validation>
            <v-row>
              <v-col cols="12">
                <h2>Identification</h2>
              </v-col>
              <v-col cols="12" sm="6" md="4">
                <v-text-field label="Alias" autocomplete="nope" hint="Identifiant du profil"></v-text-field>
              </v-col>
              <v-col cols="12" sm="6" md="4">
                <v-text-field
                  v-model="prenom"
                  label="Prénom*"
                  autocomplete="nope"
                  hint="Prénom du profil à créer"
                  :rules="prenomRules"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6" md="4">
                <v-text-field
                  v-model="nom"
                  label="Nom*"
                  autocomplete="nope"
                  hint="Nom du profil à créer"
                  :rules="nomRules"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <h2>Profil sociologique</h2>
              </v-col>
              <v-col cols="12" sm="6" md="4">
                <v-text-field
                  v-model="age"
                  label="Age*"
                  type="number"
                  autocomplete="nope"
                  hint="Age du profil"
                  :rules="ageRules"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6">
                <v-select :items="['Non spécifié', 'Homme', 'Femme']" label="Sexe*" required></v-select>
              </v-col>
              <v-col cols="12" sm="6">
                <v-select
                  :items="['Non spécifié', 'Primaire', 'Secondaire 1', 'Secondaire 2', 'Supérieur']"
                  label="Niveau d'éducation"
                ></v-select>
              </v-col>
              <v-col cols="12" sm="6">
                <v-select
                  :items="['Non spécifiée', 'Classe populaire', 'Classe moyenne', 'Classe aisée']"
                  label="Classe sociale"
                ></v-select>
              </v-col>
              <v-col cols="12">
                <h2>Informations complémentaires</h2>
              </v-col>
              <v-col cols="12">
                <v-textarea autocomplete="nope" label="Commentaires"></v-textarea>
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-btn color="blue darken-1" text @click="checkDialog">Fermer</v-btn>
          <v-btn color="blue darken-1" :disabled="!valid" text @click="validate">Créer</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
export default {
  name: "CreateProfilConnu",
  data: () => ({
    dialogm1: "",
    dialog: false,
    valid: true,
    nom: "",
    nomRules: [v => !!v || "Le nom est requis."],
    prenom: "",
    prenomRules: [v => !!v || "Le prénom est requis."],
    age: "",
    ageRules: [
      v => !!v || "L'âge est requis.",
      v =>
        /^(([9])|([1-9][0-9])|([1][0-1][0-9])|120)$/.test(v) ||
        "L'âge doit être compris entre 9 et 120"
    ]
  }),
  methods: {
    checkDialog() {
      this.dialog = !this.dialog;
    },
    validate() {
      if (this.$refs.form.validate()) {
        alert("Le profil à bien été crée");
        this.reset();
        this.dialog = false;
      }
    },
    reset() {
      this.$refs.form.reset();
    },
    resetValidation() {
      this.$refs.form.resetValidation();
    }
  }
};
</script>