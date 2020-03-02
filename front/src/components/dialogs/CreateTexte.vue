<template>
  <v-row justify="center">
    <v-dialog v-model="data.texte" persistent scrollable max-width="500px">
      <v-card>
        <v-card-title>Importer un texte</v-card-title>
        <v-divider></v-divider>
        <v-card-text style="height: 300px;">
          <v-form ref="form" v-model="valid" lazy-validation>
            <v-row>
              <v-col cols="12">
                <h2>Importation</h2>
              </v-col>
              <v-col cols="12">
                <input accept=".txt" type="file" id="file" ref="file" @change="handleFileUpload()" />
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-btn color="blue darken-1" text @click="checkDialog">Fermer</v-btn>
          <v-btn color="blue darken-1" :disabled="!valid" text @click="validate">Importer le texte</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import { DialogsData } from "../../flux/Dialogs";
import axios from "axios";

export default {
  name: "CreateTexte",
  data: () => ({
    data: DialogsData.state,
    file: "",
    connu: true,
    dialogm1: "",
    dialog: false,
    valid: true,
    alias: "",
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
    ],
    ageTexte: "Âge",
    ageType: "number",
    sexe: "Non spécifié",
    education: "Non spécifié",
    sociale: "Non spécifiée",
    commentaire: ""
  }),
  methods: {
    checkDialog() {
      DialogsData.close("texte");
    },
    reset() {
      this.$refs.form.reset();
    },
    changerType() {
      this.connu = !this.connu;
      // Changement du rôle de l'âge
      if (this.connu === true) {
        this.ageRules = [
          v => !!v || "L'âge est requis.",
          v =>
            /^(([9])|([1-9][0-9])|([1][0-1][0-9])|120)$/.test(v) ||
            "L'âge doit être compris entre 9 et 120"
        ];
        this.ageTexte = "Âge*";
        this.ageType = "number";
      } else {
        this.ageRules = [
          v => !!v || "L'âge estimé est requis.",
          v =>
            /^[1-9][0-9][-](([1-9])|([1-9][0-9])|([1][0-1][0-9])|120)$/.test(
              v
            ) ||
            "L'âge doit être estimé. Exemple de saisie : 25-30. La plage de saisie va de 10 à 120."
        ];
        this.ageTexte = "Estimation de l'âge";
        this.ageType = "text";
      }
    },
    handleFileUpload() {
      this.file = this.$refs.file.files[0];
    },
    validate() {
      if (this.$refs.form.validate()) {
        let formData = new FormData();
        formData.append("importer-texte", this.file);

        // Verifier l'upload
        // Appel avec axios
        axios
          .post(process.env.VUE_APP_SERVEUR + "/verifier-texte", formData, {
            headers: {
              "Content-Type": "multipart/form-data"
            }
          })
          .then(response => {
            alert("Le profil à bien été crée");
            console.log(response);
            this.reset();
            //DialogsData.close("profil-connu");
          })
          .catch(error => {
            console.log(error);
          });
      }
    },
    resetValidation() {
      this.$refs.form.resetValidation();
      this.sexe = "Non spécifié";
      this.education = "Non spécifié";
      this.sociale = "Non spécifiée";
    }
  }
};
</script>
