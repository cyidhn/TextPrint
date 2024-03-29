<template>
  <v-row justify="center">
    <v-dialog
      v-model="data.profilAnonyme"
      persistent
      scrollable
      max-width="500px"
    >
      <v-card>
        <div v-if="connu">
          <v-card-title>Créer un profil connu</v-card-title>
        </div>
        <div v-else>
          <v-card-title>Créer un profil anonyme</v-card-title>
        </div>
        <v-divider></v-divider>
        <v-card-text style="height: 300px;">
          <v-form ref="form" v-model="valid" lazy-validation>
            <v-row>
              <v-col cols="12">
                <h2>Identification</h2>
              </v-col>
              <v-col cols="12" sm="6" md="4">
                <v-text-field
                  v-model="alias"
                  label="Alias"
                  autocomplete="nope"
                  hint="Identifiant du profil"
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6" md="4" v-if="connu">
                <v-text-field
                  v-model="prenom"
                  label="Prénom*"
                  autocomplete="nope"
                  hint="Prénom du profil à créer"
                  :rules="prenomRules"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6" md="4" v-if="connu">
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
                  :label="ageTexte"
                  :type="ageType"
                  autocomplete="nopep"
                  hint="Âge du profil"
                  :rules="ageRules"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6">
                <v-select
                  :items="['Non spécifié', 'Homme', 'Femme']"
                  v-model="sexe"
                  label="Sexe"
                  required
                ></v-select>
              </v-col>
              <v-col cols="12" sm="6">
                <v-select
                  :items="[
                    'Non spécifié',
                    'Primaire',
                    'Secondaire 1',
                    'Secondaire 2',
                    'Supérieur',
                  ]"
                  v-model="education"
                  label="Niveau d'éducation"
                ></v-select>
              </v-col>
              <v-col cols="12" sm="6">
                <v-select
                  :items="[
                    'Non spécifiée',
                    'Classe populaire',
                    'Classe moyenne',
                    'Classe aisée',
                  ]"
                  v-model="sociale"
                  label="Classe sociale"
                ></v-select>
              </v-col>
              <v-col cols="12">
                <h2>Informations complémentaires</h2>
              </v-col>
              <v-col cols="12">
                <v-textarea
                  v-model="commentaire"
                  autocomplete="nope"
                  label="Commentaires"
                ></v-textarea>
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-btn
            v-shortkey="['ctrl', 'x']"
            @shortkey="checkDialog"
            color="blue darken-1"
            text
            @click="checkDialog"
            >Fermer</v-btn
          >
          <v-btn color="blue darken-1" text @click="changerType" v-if="connu"
            >Changer à profil anonyme</v-btn
          >
          <v-btn color="blue darken-1" text @click="changerType" v-if="!connu"
            >Changer à profil connu</v-btn
          >
          <v-btn color="blue darken-1" :disabled="!valid" text @click="validate"
            >Créer</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
// Importations
import { DialogsData } from "../../flux/Dialogs";
import axios from "axios";

// Exportation de la fonction
export default {
  name: "CreateProfilAnonyme",
  data: () => ({
    data: DialogsData.state,
    connu: false,
    dialogm1: "",
    dialog: false,
    valid: true,
    alias: "",
    nom: "",
    nomRules: [(v) => !!v || "Le nom est requis."],
    prenom: "",
    prenomRules: [(v) => !!v || "Le prénom est requis."],
    age: "",
    ageRules: [
      (v) => !!v || "L'âge estimé est requis.",
      (v) =>
        /^[1-9][0-9][-](([1-9])|([1-9][0-9])|([1][0-1][0-9])|120)$/.test(v) ||
        "L'âge doit être estimé. Exemple de saisie : 25-30. La plage de saisie va de 10 à 120.",
      (v) =>
        this.testAgeAnonyme(v) ||
        "L'âge à gauche doit être plus petite qu'à droite...",
    ],
    ageTexte: "Âge",
    ageType: "number",
    sexe: "Non spécifié",
    education: "Non spécifié",
    sociale: "Non spécifiée",
    commentaire: "",
  }),
  mounted: function () {
    this.ageRules = [
      (v) => !!v || "L'âge estimé est requis.",
      (v) =>
        /^[1-9][0-9][-](([1-9])|([1-9][0-9])|([1][0-1][0-9])|120)$/.test(v) ||
        "L'âge doit être estimé. Exemple de saisie : 25-30. La plage de saisie va de 10 à 120.",
      (v) =>
        this.testAgeAnonyme(v) ||
        "L'âge à gauche doit être plus petite qu'à droite...",
    ];
    this.ageTexte = "Estimation de l'âge";
    this.ageType = "text";
  },
  methods: {
    testAgeAnonyme(v) {
      // Split
      let splitNumber = v.split("-");
      // Verification
      if (
        Number(splitNumber[0]) > Number(splitNumber[1]) ||
        Number(splitNumber[0]) == Number(splitNumber[1])
      ) {
        return false;
      } else {
        return true;
      }
    },
    checkDialog() {
      DialogsData.close("profil-anonyme");
    },
    reset() {
      this.$refs.form.reset();
    },
    changerType() {
      this.connu = !this.connu;
      // Changement du rôle de l'âge
      if (this.connu === true) {
        this.ageRules = [
          (v) => !!v || "L'âge est requis.",
          (v) =>
            /^(([9])|([1-9][0-9])|([1][0-1][0-9])|120)$/.test(v) ||
            "L'âge doit être compris entre 9 et 120",
        ];
        this.ageTexte = "Âge*";
        this.ageType = "number";
      } else {
        this.ageRules = [
          (v) => !!v || "L'âge estimé est requis.",
          (v) =>
            /^[1-9][0-9][-](([1-9])|([1-9][0-9])|([1][0-1][0-9])|120)$/.test(
              v
            ) ||
            "L'âge doit être estimé. Exemple de saisie : 25-30. La plage de saisie va de 10 à 120.",
        ];
        this.ageTexte = "Estimation de l'âge*";
        this.ageType = "text";
      }
    },
    validate() {
      if (this.$refs.form.validate()) {
        // Ajout en formulaire
        let formData = new FormData();
        if (
          (this.alias == "" || this.alias == undefined) &&
          this.connu == false
        ) {
          this.alias = "J.Dupont_" + Date.now();
        }
        formData.append("alias", this.alias);
        formData.append("prenom", this.prenom);
        formData.append("nom", this.nom);
        formData.append("age", this.age);
        formData.append("sexe", this.sexe);
        formData.append("education", this.education);
        formData.append("sociale", this.sociale);
        formData.append("commentaire", this.commentaire);
        // Profil connu ou non
        if (this.connu === true) {
          formData.append("typeP", "connu");
        } else {
          formData.append("typeP", "anonyme");
        }

        // Appel avec axios
        axios
          .post(process.env.VUE_APP_SERVEUR + "/creer-profil-connu", formData)
          .then((response) => {
            // Message profil bien crée
            alert("Le profil à bien été crée");
            console.log(response);
            this.reset();
            DialogsData.close("profil-connu");
          })
          .catch((error) => {
            // Affichage erreur
            console.log(error);
          });
      }
    },
    resetValidation() {
      // Reset informations mis en mémoire
      this.$refs.form.resetValidation();
      this.sexe = "Non spécifié";
      this.education = "Non spécifié";
      this.sociale = "Non spécifiée";
    },
  },
};
</script>
