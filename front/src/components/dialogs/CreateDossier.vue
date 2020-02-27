<template>
  <v-row justify="center">
    <v-dialog v-model="data.dossier" persistent scrollable max-width="500px">
      <v-card>
        <v-card-title>Créer un nouveau dossier</v-card-title>
        <v-divider></v-divider>
        <v-card-text style="height: 150px;">
          <v-form ref="form" v-model="valid" lazy-validation>
            <v-row>
              <v-col cols="12">
                <v-text-field
                  v-model="nom"
                  label="Titre du dossier*"
                  autocomplete="nope"
                  hint="Donner un nom unique à votre nouveau dossier."
                  :rules="nomRules"
                  required
                ></v-text-field>
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
import { DialogsData } from "../../flux/Dialogs";
import axios from "axios";

export default {
  name: "CreateDossier",
  data: () => ({
    data: DialogsData.state,
    dialogm1: "",
    dialog: false,
    valid: true,
    nom: "",
    nomRules: [v => !!v || "Le nom du dossier est requis."]
  }),
  methods: {
    checkDialog() {
      DialogsData.close("dossier");
    },
    reset() {
      this.$refs.form.reset();
    },
    validate() {
      if (this.$refs.form.validate()) {
        // Ajout en formulaire
        let formData = new FormData();
        formData.append("titre", this.nom);

        // Appel avec axios
        axios
          .post(process.env.VUE_APP_SERVEUR + "/creer-dossier", formData)
          .then(response => {
            alert("Le dossier a bien été crée");
            console.log(response);
            this.reset();
            DialogsData.close("dossier");
          })
          .catch(error => {
            alert(error.response.data);
          });
      }
    },
    resetValidation() {
      this.$refs.form.resetValidation();
    }
  }
};
</script>
