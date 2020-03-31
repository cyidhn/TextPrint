<template>
  <div>
    <h1>Profil {{ formulaire.typeP }} : {{ identification }}</h1>
    <v-container fluid class="mt-8">
      <v-row v-if="formulaire.typeP === 'connu'">
        <v-col cols="12">
          <v-btn
            class="mr-3"
            depressed
            small
            color="primary"
            @click="changeTypeProfil"
            >Change à profil anonyme</v-btn
          >
          <v-btn @click="removeProfil" depressed small color="error"
            >Supprimer</v-btn
          >
        </v-col>
      </v-row>
      <v-row v-else>
        <v-col cols="12">
          <v-btn
            class="mr-3"
            depressed
            small
            color="primary"
            @click="changeTypeProfil"
            >Change à profil connu</v-btn
          >
          <v-btn @click="removeProfil" depressed small color="error"
            >Supprimer</v-btn
          >
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" align="start">
          <h2>Identification</h2>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="6" align="start">
          <v-text-field
            v-model="formulaire.alias"
            autocomplete="nope"
            label="Alias"
            required
          ></v-text-field>
        </v-col>
      </v-row>
      <div v-if="formulaire.typeP === 'connu'">
        <v-row>
          <v-col cols="6" align="start">
            <v-text-field
              v-model="formulaire.prenom"
              autocomplete="nope"
              label="Prénom*"
              required
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="6" align="start">
            <v-text-field
              v-model="formulaire.nom"
              autocomplete="nope"
              label="Nom*"
              required
            ></v-text-field>
          </v-col>
        </v-row>
      </div>
      <v-row class="mt-8">
        <v-col cols="12" align="start">
          <h2>Profil Sociologique</h2>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="6" align="start">
          <v-text-field
            v-model="formulaire.age"
            autocomplete="nope"
            label="Age"
            required
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="6" align="start">
          <v-select
            v-model="formulaire.sexe"
            :items="['Non spécifié', 'Homme', 'Femme']"
            label="Sexe*"
            required
          ></v-select>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="6" align="start">
          <v-select
            v-model="formulaire.education"
            :items="[
              'Non spécifié',
              'Primaire',
              'Secondaire 1',
              'Secondaire 2',
              'Supérieur'
            ]"
            label="Niveau d'éducation"
            required
          ></v-select>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="6" align="start">
          <v-select
            v-model="formulaire.sociale"
            :items="[
              'Non spécifiée',
              'Classe populaire',
              'Classe moyenne',
              'Classe aisée'
            ]"
            label="Classe sociale"
            required
          ></v-select>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" align="start">
          <h2>Informations complémentaires</h2>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="6" align="start">
          <v-textarea
            v-model="formulaire.commentaire"
            label="Commentaire"
            required
          ></v-textarea>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="6" align="start">
          <v-btn block color="error" class="mt-4" @click="modifierProfil"
            >Sauvegarder</v-btn
          >
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
// Importations
import axios from "axios";
import { TabsData } from "../../flux/Tabs";

// Exportation de la fonction
export default {
  props: {
    content: Object,
    personne: String
  },

  data: () => ({
    formulaire: [],
    identification: ""
  }),

  methods: {
    changeTypeProfil() {
      if (confirm("Êtes-vous sûr de vouloir changer le type de profil ?")) {
        // Contenu des fichiers
        let formData = new FormData();
        formData.append("id", this.content.id);
        formData.append("type", this.formulaire.typeP);

        // Appel avec axios
        axios
          .post(process.env.VUE_APP_SERVEUR + "/changer-type-profil", formData)
          .then(response => {
            if (this.formulaire.typeP == "connu") {
              this.formulaire.typeP = "anonyme";
            } else {
              this.formulaire.typeP = "connu";
            }
            alert("Le type de profil a bien été modifié");
            console.log(response);
          })
          .catch(error => {
            alert(error);
          });
      }
    },
    modifierProfil() {
      // Contenu des fichiers
      let formData = new FormData();
      formData.append("id", this.content.id);
      formData.append("alias", this.formulaire.alias);
      formData.append("prenom", this.formulaire.prenom);
      formData.append("nom", this.formulaire.nom);
      formData.append("age", this.formulaire.age);
      formData.append("sexe", this.formulaire.sexe);
      formData.append("education", this.formulaire.education);
      formData.append("sociale", this.formulaire.sociale);
      formData.append("commentaire", this.formulaire.commentaire);

      // Appel avec axios
      axios
        .post(process.env.VUE_APP_SERVEUR + "/modifier-profil", formData)
        .then(response => {
          alert("Sauvegarde effectuée");
          console.log(response);
        })
        .catch(error => {
          alert(error);
        });
    },
    removeProfil() {
      if (
        confirm(
          "Voulez-vous vraiment supprimer ce profil et ses analyses définitivement ?"
        )
      ) {
        // Appel avec axios
        let formData = new FormData();
        formData.append("id", this.content.id);
        axios
          .post(process.env.VUE_APP_SERVEUR + "/supprimer-profil", formData)
          .then(response => {
            alert("Le profil a bien été supprimé");
            TabsData.remove(TabsData.state.nowId);
            console.log(response);
          })
          .catch(error => {
            alert(error);
          });
      }
    },
    fetchProps() {
      this.formulaire = this.content;
      if (
        this.formulaire.alias === undefined ||
        this.formulaire.alias === "undefined" ||
        this.formulaire.alias === ""
      ) {
        this.formulaire.alias = "";
        this.identification =
          this.formulaire.prenom + " " + this.formulaire.nom;
      } else {
        this.identification = this.formulaire.alias;
      }
    },
    modifsOldVersion() {
      // Champs sexe
      if (this.formulaire.sexe === "femme") {
        this.formulaire.sexe = "Femme";
      }

      if (this.formulaire.sexe === "homme") {
        this.formulaire.sexe = "Homme";
      }

      if (this.formulaire.sexe === "non spécifié") {
        this.formulaire.sexe = "Non spécifié";
      }

      // Champs age
      if (this.formulaire.age === "Non spécifié") {
        this.formulaire.age = 20;
      }

      // Champs niveau d'éducation
      if (this.formulaire.education === "no ") {
        this.formulaire.education = "Non spécifié";
      }

      if (this.formulaire.education === "primaire") {
        this.formulaire.education = "Primaire";
      }

      if (this.formulaire.education === "secondaire-1") {
        this.formulaire.education = "Secondaire 1";
      }

      if (this.formulaire.education === "secondaire-2") {
        this.formulaire.education = "Secondaire 2";
      }

      if (this.formulaire.education === "superieur") {
        this.formulaire.education = "Supérieur";
      }

      // Champs classe sociale
      if (this.formulaire.sociale === "no") {
        this.formulaire.sociale = "Non spécifiée";
      }

      if (this.formulaire.sociale === "populaire") {
        this.formulaire.sociale = "Classe populaire";
      }

      if (this.formulaire.sociale === "moyenne") {
        this.formulaire.sociale = "Classe moyenne";
      }

      if (this.formulaire.sociale === "aisée") {
        this.formulaire.sociale = "Classe aisée";
      }

      if (this.formulaire.commentaire === "undefined") {
        this.formulaire.commentaire = "";
      }
    }
  },

  mounted() {
    // Anciennes modifications
    this.fetchProps();
    this.modifsOldVersion();
  }
};
</script>
