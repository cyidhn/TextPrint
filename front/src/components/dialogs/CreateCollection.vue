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
          <v-btn
            text
            v-shortkey="['ctrl', 'x']"
            @shortkey="checkDialog"
            color="blue darken-1"
            @click="checkDialog"
            >Fermer</v-btn
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
import { TabsData } from "../../flux/Tabs";
import { AddData } from "../../flux/Add";
import axios from "axios";

// Exportation de la fonction
export default {
  name: "CreateCollection",
  data: () => ({
    data: DialogsData.state,
    dialogm1: "",
    dialog: false,
    valid: true,
    nom: "",
    nomRules: [(v) => !!v || "Le nom de la collection est requise."],
  }),
  methods: {
    addWindow() {
      // Ajout en formulaire
      let formData = new FormData();

      // Appel avec axios
      axios
        .get(process.env.VUE_APP_SERVEUR + "/lastid-collection")
        .then((response) => {
          formData.append("req", response.data[0].id);
          console.log(response.data[0].id);
          axios
            .post(process.env.VUE_APP_SERVEUR + "/search-collection", formData)
            .then((response2) => {
              console.log(response2);
              AddData.open();
              TabsData.add(response2.data[0].titre, response2.data[0]);
            })
            .catch((error) => {
              alert(error.response.data);
            });
        })
        .catch((error) => {
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
          .then((response) => {
            // begin
            // Appel avec axios
            axios
              .get(process.env.VUE_APP_SERVEUR + "/lastid-collection")
              .then((response) => {
                let idCollection = response.data[0].id;
                console.log(idCollection);
                // Si le folder est activé
                if (DialogsData.state.stateInFolder == true) {
                  console.log("ok");
                  formData = new FormData();
                  formData.append("champs1", DialogsData.state.nameFolder);
                  formData.append("champs2", "Collection");
                  formData.append("idchamps1", DialogsData.state.numberFolder);
                  formData.append("idchamps2", idCollection);
                  // Appel avec axios
                  axios
                    .post(
                      process.env.VUE_APP_SERVEUR + "/associer-generalement",
                      formData
                    )
                    .then((response) => {
                      if (
                        confirm(
                          "La collection a bien été créée. Souhaitez-vous ajouter des éléments maintenant à celle-ci ?"
                        )
                      ) {
                        this.addWindow();
                      } else {
                        alert("La collection à bien été créée et ajoutée.");
                      }
                      console.log(response.data);
                    })
                    .catch((error) => {
                      console.error(error);
                    });
                } else {
                  if (
                    confirm(
                      "La collection a bien été créée. Souhaitez-vous ajouter des éléments maintenant à celle-ci ?"
                    )
                  ) {
                    this.addWindow();
                  }
                }
              })
              .catch((error) => {
                alert(error.response.data);
              });
            // end
            console.log(response);
            this.reset();
            DialogsData.close("collection");
          })
          .catch((error) => {
            alert(error.response.data);
          });
      }
    },
    resetValidation() {
      this.$refs.form.resetValidation();
    },
  },
};
</script>
