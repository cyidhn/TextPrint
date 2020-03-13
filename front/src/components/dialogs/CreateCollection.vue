<template>
  <v-row justify="center">
    <v-dialog v-model="data.collection" persistent scrollable max-width="500px">
      <v-card>
        <v-card-title>Créer une nouvelle collection</v-card-title>
        <v-divider></v-divider>
        <v-card-text style="height: 150px;">
          <v-form ref="form" v-model="valid" lazy-validation>
            <v-row>
              <v-col cols="12">
                <v-text-field
                  v-model="nom"
                  label="Titre de la collection*"
                  autocomplete="nope"
                  hint="Donner un nom unique à votre nouvelle collection."
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
import { TabsData } from "../../flux/Tabs";
import axios from "axios";

export default {
  name: "CreateCollection",
  data: () => ({
    data: DialogsData.state,
    dialogm1: "",
    dialog: false,
    valid: true,
    nom: "",
    nomRules: [v => !!v || "Le nom de la collection est requis."]
  }),
  methods: {
    addWindow() {
      // Ajout en formulaire
      let formData = new FormData();

      // Appel avec axios
      axios
        .get(process.env.VUE_APP_SERVEUR + "/lastid-collection")
        .then(response => {
          formData.append("req", response.data[0].id);
          console.log(response.data[0].id);
          axios
            .post(process.env.VUE_APP_SERVEUR + "/search-collection", formData)
            .then(response2 => {
              console.log(response2);
              TabsData.add(response2.data[0].titre, response2.data[0]);
            })
            .catch(error => {
              alert(error.response.data);
            });
        })
        .catch(error => {
          alert(error.response.data);
        });
    },
    checkDialog() {
      DialogsData.close("collection");
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
          .post(process.env.VUE_APP_SERVEUR + "/creer-collection", formData)
          .then(response => {
            if (
              confirm(
                "La collection a bien été créée. Souhaitez-vous ajoutez des éléments maintenant à celle-ci ?"
              )
            ) {
              this.addWindow();
            }
            console.log(response);
            this.reset();
            DialogsData.close("collection");
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
