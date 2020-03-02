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
              <v-col cols="12" class="mt-8">
                <h2>Mise en forme</h2>
              </v-col>
              <v-col cols="12">
                <v-select
                  :items="['Non spécifié', 
                  'Écriture personnelle', 
                  'Correspondance', 
                  'Messagerie', 
                  'Web et réseaux sociaux', 
                  'Presse', 
                  'Rédactions Scientifiques et Académiques', 
                  'Rédactions littéraires',
                  'Rédactions judiciaires',
                  'Documents à intérêts judiciaires',
                  'Autre']"
                  v-model="typeDoc1"
                  label="Type de document*"
                  @change="handleChangeType1()"
                  required
                ></v-select>
                <v-select
                  v-if="viewTypeDoc2"
                  :items="getTypeDoc2"
                  v-model="typeDoc2"
                  @change="handleChangeType2()"
                  required
                ></v-select>
                <v-text-field
                  v-if="viewTypeDocAutre"
                  v-model="typeDocAutre"
                  label="Saisir le type du document"
                  autocomplete="nope"
                  required
                ></v-text-field>
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
    getTypeDoc2: [],
    viewTypeDoc2: false,
    typeDoc2: "",
    viewTypeDoc3: false,
    getTypeDoc3: [],
    typeDoc3: "",
    viewTypeDocAutre: false,
    typeDocAutre: "",
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
    handleChangeType1() {
      // Non spécifié
      if (this.typeDoc1 === "Non spécifié") {
        // Masquer les éléments
        this.viewTypeDoc2 = false;
        this.viewTypeDoc3 = false;
        this.viewTypeDocAutre = false;
      }

      // Autre
      if (this.typeDoc1 === "Autre") {
        // Masquer les éléments
        this.viewTypeDoc2 = false;
        this.viewTypeDoc3 = false;

        // Afficher le champs autre
        this.viewTypeDocAutre = true;
      }

      // Écriture personnelle
      if (this.typeDoc1 === "Écriture personnelle") {
        // Afficher les éléments
        this.viewTypeDoc2 = true;
        this.viewTypeDoc3 = false;
        this.viewTypeDocAutre = false;

        // Enregistre élément dans le select
        this.getTypeDoc2 = [
          "Jounal / Entrée d'un journal",
          "Notes personnelles",
          "Autre"
        ];
        this.typeDoc2 = this.getTypeDoc2[0];
      }

      // Correspondance
      if (this.typeDoc1 === "Correspondance") {
        // Afficher les éléments
        this.viewTypeDoc2 = true;
        this.viewTypeDoc3 = false;
        this.viewTypeDocAutre = false;

        // Enregistre élément dans le select
        this.getTypeDoc2 = [
          "Note",
          "Carte postale",
          "Lettre",
          "Email",
          "Autre"
        ];
        this.typeDoc2 = this.getTypeDoc2[0];
      }

      // Messagerie
      if (this.typeDoc1 === "Messagerie") {
        // Afficher les éléments
        this.viewTypeDoc2 = true;
        this.viewTypeDoc3 = false;
        this.viewTypeDocAutre = false;

        // Enregistre élément dans le select
        this.getTypeDoc2 = ["SMS", "Messagerie instantanée", "Autre"];
        this.typeDoc2 = this.getTypeDoc2[0];
      }

      // Web et réseaux sociaux
      if (this.typeDoc1 === "Web et réseaux sociaux") {
        // Afficher les éléments
        this.viewTypeDoc2 = true;
        this.viewTypeDoc3 = false;
        this.viewTypeDocAutre = false;

        // Enregistre élément dans le select
        this.getTypeDoc2 = [
          "Tweet",
          "Publication sur forum",
          "Publication sur Facebook",
          "Billet de blog",
          "Commentaires et interactions",
          "Autre"
        ];
        this.typeDoc2 = this.getTypeDoc2[0];
      }

      // Presse
      if (this.typeDoc1 === "Presse") {
        // Afficher les éléments
        this.viewTypeDoc2 = true;
        this.viewTypeDoc3 = false;
        this.viewTypeDocAutre = false;

        // Enregistre élément dans le select
        this.getTypeDoc2 = ["Article", "Journal", "Revue", "Autre"];
        this.typeDoc2 = this.getTypeDoc2[0];
      }

      // Rédactions Scientifiques et Académiques
      if (this.typeDoc1 === "Rédactions Scientifiques et Académiques") {
        // Afficher les éléments
        this.viewTypeDoc2 = true;
        this.viewTypeDoc3 = false;
        this.viewTypeDocAutre = false;

        // Enregistre élément dans le select
        this.getTypeDoc2 = [
          "Article",
          "Essai",
          "Dissertation",
          "Mémoire",
          "Rapport",
          "Revue scientifique",
          "Livre d'instruction",
          "Autre"
        ];
        this.typeDoc2 = this.getTypeDoc2[0];
      }

      // Rédactions littéraires
      if (this.typeDoc1 === "Rédactions littéraires") {
        // Afficher les éléments
        this.viewTypeDoc2 = true;
        this.viewTypeDoc3 = false;
        this.viewTypeDocAutre = false;

        // Enregistre élément dans le select
        this.getTypeDoc2 = [
          "Poésie",
          "Roman",
          "Pièce de théâtre",
          "Conte",
          "Fable",
          "Autobiographie ou mémoire",
          "Biographie",
          "Autre"
        ];
        this.typeDoc2 = this.getTypeDoc2[0];
      }

      // Rédactions judiciaires
      if (this.typeDoc1 === "Rédactions judiciaires") {
        // Afficher les éléments
        this.viewTypeDoc2 = true;
        this.viewTypeDoc3 = false;
        this.viewTypeDocAutre = false;

        // Enregistre élément dans le select
        this.getTypeDoc2 = ["Rapport", "Témoignage", "Lettre d'aveu", "Autre"];
        this.typeDoc2 = this.getTypeDoc2[0];
      }

      // Documents à intérêts judiciaires
      if (this.typeDoc1 === "Documents à intérêts judiciaires") {
        // Afficher les éléments
        this.viewTypeDoc2 = true;
        this.viewTypeDoc3 = false;
        this.viewTypeDocAutre = false;

        // Enregistre élément dans le select
        this.getTypeDoc2 = [
          "Lettre d'adieu",
          "Lettre de menace",
          "Demande de rançon",
          "Testament",
          "Autre"
        ];
        this.typeDoc2 = this.getTypeDoc2[0];
      }
    },
    handleChangeType2() {
      if (this.typeDoc2 === "Autre") {
        this.viewTypeDocAutre = true;
      } else {
        this.viewTypeDocAutre = false;
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
