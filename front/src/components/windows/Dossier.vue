<template>
  <div>
    <v-container fluid>
      <!-- Modal ajouter un profil -->
      <v-dialog v-model="dialogProfils" max-width="500px" persistent scrollable>
        <v-card>
          <v-card-title>
            <span class="headline">
              <b>Ajouter un profil</b>
            </span>
          </v-card-title>
          <v-card-text>
            <v-card class="mx-auto" max-width="800" tile>
              <v-text-field
                v-model="rechercheAjoutsProfils"
                label="Rechercher dans la base de données"
                required
              ></v-text-field>
              <v-data-table
                no-data-text="Aucun élément trouvé"
                no-results-text="Aucun élément trouvé"
                loading-text="Chargement en cours..."
                v-model="selectedAjoutsProfils"
                :headers="headersProfils"
                :items="filteredList"
                :items-per-page="5"
                item-key="id"
                show-select
                class="elevation-1"
              ></v-data-table>
            </v-card>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" text @click="fermerProfils">Retour</v-btn>
            <v-btn color="blue darken-1" text @click="associerProfils">Ajouter des profils</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <!-- /Modal ajouter un profil -->

      <br />
      <br />
      <v-row>
        <v-col cols="6" align="start">
          <h2>Association avec les Profils</h2>
        </v-col>
        <v-col cols="6" align="end">
          <v-btn small class="mx-2" color="primary" @click="ajouterProfils">Ajouter un profil</v-btn>
          <v-btn
            small
            color="error"
            :disabled="disabledProfils"
            @click="deleteProfils"
          >Supprimer la sélection</v-btn>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="6" align="start">
          <v-text-field
            class="mx-2"
            v-model="searchProfils"
            label="Filtrer"
            single-line
            hide-details
          ></v-text-field>
        </v-col>
      </v-row>
      <br />
      <v-data-table
        no-data-text="Aucun élément trouvé"
        no-results-text="Aucun élément trouvé"
        loading-text="Chargement en cours..."
        v-model="selectedProfils"
        :headers="headersProfils"
        :items="profils"
        :search="searchProfils"
        item-key="id"
        show-select
        class="elevation-1"
      ></v-data-table>
    </v-container>
    <v-container fluid>
      <br />
      <br />
      <v-row>
        <v-col cols="6" align="start">
          <h2>Association avec les Textes</h2>
        </v-col>
        <v-col cols="6" align="end">
          <v-btn small class="mx-2" color="primary">Ajouter un texte</v-btn>
          <v-btn small color="error" :disabled="disabledTextes">Supprimer la sélection</v-btn>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="6" align="start">
          <v-text-field
            class="mx-2"
            v-model="searchTextes"
            label="Filtrer"
            single-line
            hide-details
          ></v-text-field>
        </v-col>
      </v-row>
      <br />
      <v-data-table
        no-data-text="Aucun élément trouvé"
        no-results-text="Aucun élément trouvé"
        loading-text="Chargement en cours..."
        v-model="selectedTextes"
        :headers="headersTextes"
        :items="textes"
        :search="searchTextes"
        item-key="id"
        show-select
        class="elevation-1"
      ></v-data-table>
    </v-container>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      disabledProfils: true,
      disabledTextes: true,
      searchProfils: "",
      searchTextes: "",
      selectedProfils: [],
      selectedTextes: [],
      headersProfils: [
        { text: "Type", value: "type" },
        { text: "Alias", value: "alias" },
        { text: "Prénom NOM", value: "nom" }
      ],
      profils: [],
      headersTextes: [
        { text: "Titre", value: "titre" },
        { text: "# Versions", value: "version" }
      ],
      textes: [],
      // Ajouts profils
      dialogProfils: false,
      rechercheAjoutsProfils: "",
      selectedAjoutsProfils: [],
      contentProfils: []
    };
  },
  methods: {
    ajouterProfils() {
      let formData = new FormData();
      formData.append("req", "");
      axios
        .post(process.env.VUE_APP_SERVEUR + "/searchprofil", formData)
        .then(response => {
          this.contentProfils = response.data;
        })
        .catch(e => {
          this.getError = true;
          console.error("Impossible de charger les données", e);
        });
      this.dialogProfils = !this.dialogProfils;
      console.log("Ok");
    },
    associerProfils() {
      if (confirm("Voulez-vous vraiment ajouter cette association ?")) {
        let formData = new FormData();
        this.selectedAjoutsProfils.map(e => {
          formData = new FormData();
          formData.append("champs1", "Dossier");
          formData.append("champs2", "Profil");
          formData.append("idchamps1", 2);
          formData.append("idchamps2", e.id);
          // Appel avec axios
          axios
            .post(
              process.env.VUE_APP_SERVEUR + "/associer-generalement",
              formData
            )
            .then(response => {
              console.log(response.data);
              // TypeProfils
              // Ajout en formulaire
              let newFormData = new FormData();
              newFormData.append("id", 2);
              newFormData.append("type", "Dossier");
              newFormData.append("get", "Profil");

              // Appel avec axios
              axios
                .post(process.env.VUE_APP_SERVEUR + "/assoc", newFormData)
                .then(response => {
                  let result = JSON.parse(response.data);
                  this.profils = result;
                })
                .catch(error => {
                  this.profils = [];
                  console.log(error);
                });
              // /TypeProfils
            })
            .catch(error => {
              console.log(error);
            });
        });
        this.selectedAjoutsProfils = [];
        this.dialogProfils = false;
      }
    },
    fermerProfils() {
      this.dialogProfils = false;
    },
    deleteProfils() {
      if (confirm("Voulez-vous vraiment supprimer cette association ?")) {
        let formData = new FormData();
        this.selectedProfils.map(e => {
          formData = new FormData();
          formData.append("id", e.delete);
          // Appel avec axios
          axios
            .post(
              process.env.VUE_APP_SERVEUR + "/supprimer-association",
              formData
            )
            .then(response => {
              console.log(response);
              // TypeProfils
              // Ajout en formulaire
              let newFormData = new FormData();
              newFormData.append("id", 2);
              newFormData.append("type", "Dossier");
              newFormData.append("get", "Profil");

              // Appel avec axios
              axios
                .post(process.env.VUE_APP_SERVEUR + "/assoc", newFormData)
                .then(response => {
                  let result = JSON.parse(response.data);
                  this.profils = result;
                })
                .catch(error => {
                  this.profils = [];
                  console.log(error);
                });
              // /TypeProfils
            })
            .catch(error => {
              console.log(error);
            });
        });
        this.selectedProfils = [];
      }
    }
  },
  mounted: function() {
    // TypeProfils
    // Ajout en formulaire
    let formData = new FormData();
    formData.append("id", 2);
    formData.append("type", "Dossier");
    formData.append("get", "Profil");

    // Appel avec axios
    axios
      .post(process.env.VUE_APP_SERVEUR + "/assoc", formData)
      .then(response => {
        let result = JSON.parse(response.data);
        this.profils = result;
      })
      .catch(error => {
        console.log(error);
      });
    // /TypeProfils

    // TypeTextes
    // Ajout en formulaire
    formData = new FormData();
    formData.append("id", 2);
    formData.append("type", "Dossier");
    formData.append("get", "Texte");

    // Appel avec axios
    axios
      .post(process.env.VUE_APP_SERVEUR + "/assoc", formData)
      .then(response => {
        let result = JSON.parse(response.data);
        this.textes = result;
      })
      .catch(error => {
        console.log(error);
      });
    // /TypeTextes
  },
  updated: function() {
    // Profils
    if (this.selectedProfils.length > 0) {
      this.disabledProfils = false;
    } else {
      this.disabledProfils = true;
    }
    // Textes
    if (this.selectedTextes.length > 0) {
      this.disabledTextes = false;
    } else {
      this.disabledTextes = true;
    }
  },
  computed: {
    filteredList() {
      return this.contentProfils.filter(p => {
        try {
          return p.titre
            .toLowerCase()
            .includes(this.rechercheAjoutsProfils.toLowerCase());
        } catch {
          return p.alias
            .toLowerCase()
            .includes(this.rechercheAjoutsProfils.toLowerCase());
        }
      });
    }
  }
};
</script>
