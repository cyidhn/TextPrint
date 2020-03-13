<template>
  <div>
    <v-container>
      <v-row>
        <v-col cols="12">
          <v-btn
            @click="removeText"
            class="mr-3"
            depressed
            small
            color="primary"
            >Associer à des éléments</v-btn
          >
          <v-btn @click="removeText" depressed small color="error"
            >Supprimer</v-btn
          >
        </v-col>
      </v-row>
      <v-row class="mt-8">
        <v-col cols="6" align="start">
          <h3 class="mb-4">Texte original</h3>
          <iframe
            class="border-iframe"
            width="100%"
            height="500"
            :src="link"
          ></iframe>
        </v-col>
        <v-col cols="6" align="start">
          <h3 class="mb-4">Premières analyses</h3>
          <iframe
            class="border-iframe"
            width="100%"
            height="500"
            :src="linkAnalyse"
          ></iframe>
        </v-col>
      </v-row>
      <v-row class="mt-8">
        <v-col cols="12" class="mt-8">
          <h2>Informations</h2>
        </v-col>
        <v-col cols="12">
          <v-text-field
            v-model="content.titre"
            label="Titre du texte*"
            autocomplete="nope"
            hint="Donner un titre unique à votre nouveau texte."
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
            :items="[
              'Non spécifié',
              'Écriture personnelle',
              'Correspondance',
              'Messagerie',
              'Web et réseaux sociaux',
              'Presse',
              'Rédactions Scientifiques et Académiques',
              'Rédactions littéraires',
              'Rédactions judiciaires',
              'Documents à intérêts judiciaires',
              'Autre'
            ]"
            v-model="content.typeDocument1"
            label="Type de document*"
            @change="changeForm()"
            required
          ></v-select>
          <v-select
            :items="[content.typeDocument2]"
            v-model="content.typeDocument2"
            @change="changeForm()"
            required
          ></v-select>
          <v-text-field
            v-model="content.typeDocument3"
            label="Autre..."
            autocomplete="nope"
            required
          ></v-text-field>
          <v-text-field
            v-model="content.specification"
            label="Spécification"
            autocomplete="nope"
            required
          ></v-text-field>
          <v-select
            :items="[
              'Non spécifié',
              'Manuscrite',
              'Tapuscrite',
              'Dactylographié',
              'Autre'
            ]"
            v-model="content.typeEcriture"
            label="Type d'écriture"
            required
          ></v-select>
          <v-select
            :items="['Non spécifiée', 'D\'origine', 'Passage', 'Compilation']"
            v-model="content.segmentation"
            label="Segmentation"
            required
          ></v-select>
        </v-col>
        <v-col cols="12" class="mt-8">
          <h2>Description linguistique</h2>
        </v-col>
        <v-col cols="12">
          <v-select
            :items="['Non spécifiée', 'Français', 'Anglais', 'Espagnol']"
            v-model="content.langue"
            label="Langue (automatique)"
            required
          ></v-select>
          <v-select
            :items="['Non spécifié', 'Courant', 'Familier', 'Soutenu']"
            v-model="content.registre"
            label="Registre"
            required
          ></v-select>
          <v-textarea
            v-model="content.commentaire"
            autocomplete="nope"
            label="Commentaires"
          ></v-textarea>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import axios from "axios";
import { TabsData } from "../../flux/Tabs";

export default {
  props: {
    content: Object
  },
  data: () => ({
    titre: "",
    paternite: "",
    linkAnalyse: "",
    link: ""
  }),
  methods: {
    changeForm() {
      console.log("Changement dans le formulaire...");
    },
    removeText() {
      console.log(this.content.id);
      console.log(this.content);
      if (
        confirm(
          "Voulez-vous vraiment supprimer ce texte et ses analyses définitivement ?"
        )
      ) {
        // Appel avec axios
        let formData = new FormData();
        formData.append("id", this.content.id);
        axios
          .post(process.env.VUE_APP_SERVEUR + "/supprimer-texte", formData)
          .then(response => {
            alert("Le texte a bien été supprimé");
            TabsData.remove(TabsData.state.nowId);
            console.log(response);
          })
          .catch(error => {
            alert(error);
          });
      }
    }
  },
  mounted() {
    console.log(this.content);
    this.titre = this.content.titre;
    this.paternite = this.content.paternite;
    this.link =
      process.env.VUE_APP_SERVEUR +
      "/static/textes/" +
      this.content.fichier +
      ".txt";

    this.linkAnalyse =
      process.env.VUE_APP_SERVEUR +
      "/static/textes/" +
      this.content.fichier +
      "_analyse.html";
  }
};
</script>

<style scoped>
.border-iframe {
  border: 1px black solid;
}
</style>
