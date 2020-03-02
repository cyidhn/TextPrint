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
                <input accept=".txt" type="file" ref="file" @change="handleFileUpload()" />
                <p
                  v-if="loadingText"
                >Le fichier est en cours d'analyse. Cela peut prendre plusieurs minutes...</p>
                <p v-if="errorText">
                  <b>Le fichier est non conforme.</b> Merci de sélectionner un autre texte.
                </p>
              </v-col>
            </v-row>
            <v-row v-if="nextStep">
              <v-col cols="12" class="mt-8">
                <h2>Informations</h2>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  v-model="nom"
                  label="Titre du texte*"
                  autocomplete="nope"
                  hint="Donner un titre unique à votre nouveau texte."
                  :rules="nomRules"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-select
                  :items="['Non spécifié', 'Anonyme', 'Connu']"
                  v-model="paternite"
                  label="Type de paternité*"
                  required
                ></v-select>
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
    // State
    data: DialogsData.state,
    // Emplacement du fichier
    file: "",
    // Gestion des erreurs du texte
    errorText: false,
    loadingText: false,
    nextStep: false,
    disabledImport: false,
    dialogm1: "",
    dialog: false,
    valid: true,
    // Titre
    nom: "",
    nomRules: [v => !!v || "Le titre est requis."],
    // Paternité
    paternite: "Non spécifié",
    paterniteRules: [v => !!v || "Le type de paternité est requis."],
    // Type de document
    typeDoc1: "Non spécifié",
    typeDoc2: "",
    typeDoc3: "",
    // Spécification
    specification: "",
    // Type d'écriture
    typeEcriture: "Non spécifié",
    // Segmentation
    segmentation: "Non spécifiée",
    // Langue
    langue: "",
    // Registre
    registre: "Non spécifié",
    // Commentaire
    commenaire: "",
    // Model pour l'âge
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
      DialogsData.close("texte");
      this.reset();
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
        this.loadingText = true;
        this.disabledImport = true;
        this.errorText = false;
        // Verifier l'upload
        // Appel avec axios
        axios
          .post(process.env.VUE_APP_SERVEUR + "/verifier-texte", formData, {
            headers: {
              "Content-Type": "multipart/form-data"
            }
          })
          .then(response => {
            console.log(response);
            this.loadingText = false;
            this.errorText = false;
            this.nextStep = true;
            //DialogsData.close("profil-connu");
          })
          .catch(error => {
            console.log(error);
            this.loadingText = false;
            this.errorText = true;
            this.disabledImport = false;
          });
      }
    },
    resetValidation() {
      this.$refs.form.resetValidation();
      this.sexe = "Non spécifié";
      this.education = "Non spécifié";
      this.sociale = "Non spécifiée";
      this.disabledImport = false;
    }
  }
};
</script>
