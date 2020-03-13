<template>
  <div>
    <v-container fluid>
      <!-- Snackbar Ajouté avec succès -->
      <v-snackbar
        v-model="snackbarAjoute"
        :bottom="true"
        color="success"
        :timeout="3000"
      >
        Les éléments ont bien été ajoutés et sauvegardés.
        <v-btn dark text @click="snackbarAjoute = false">Fermer</v-btn>
      </v-snackbar>
      <!-- /Snackbar Ajouté avec succès -->
      <!-- Snackbar Ajouté avec succès -->
      <v-snackbar
        v-model="snackbarModifie"
        :bottom="true"
        color="success"
        :timeout="3000"
      >
        La modification a bien été prise en compte.
        <v-btn dark text @click="snackbarModifie = false">Fermer</v-btn>
      </v-snackbar>
      <!-- /Snackbar Ajouté avec succès -->
      <!-- Snackbar Supprimé avec succès -->
      <v-snackbar
        v-model="snackbarSupprimer"
        :bottom="true"
        color="error"
        :timeout="3000"
      >
        Les éléments ont bien été supprimés.
        <v-btn dark text @click="snackbarSupprimer = false">Fermer</v-btn>
      </v-snackbar>
      <!-- /Snackbar Supprimé avec succès -->
      <!-- Modal ajouter un texte -->
      <v-dialog v-model="dialogTextes" max-width="500px" persistent scrollable>
        <v-card>
          <v-card-title>
            <span class="headline">
              <b>Ajouter des textes</b>
            </span>
          </v-card-title>
          <v-card-text>
            <v-card class="mx-auto" max-width="800" tile>
              <v-text-field
                v-model="rechercheAjoutsTextes"
                label="Rechercher dans la base de données"
                required
              ></v-text-field>
              <v-data-table
                no-data-text="Aucun élément trouvé"
                no-results-text="Aucun élément trouvé"
                loading-text="Chargement en cours..."
                v-model="selectedAjoutsTextes"
                :headers="headersTextes"
                :items="filteredListTextes"
                :items-per-page="5"
                item-key="id"
                show-select
                class="elevation-1"
              ></v-data-table>
            </v-card>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" text @click="dialogTextes = false"
              >Retour</v-btn
            >
            <v-btn color="blue darken-1" text @click="associerTextes"
              >Ajouter des textes</v-btn
            >
          </v-card-actions>
        </v-card>
      </v-dialog>
      <!-- /Modal ajouter un texte -->
      <!-- Modal ajouter un profil -->
      <v-dialog v-model="dialogProfils" max-width="500px" persistent scrollable>
        <v-card>
          <v-card-title>
            <span class="headline">
              <b>Ajouter des profils</b>
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
            <v-btn color="blue darken-1" text @click="fermerProfils"
              >Retour</v-btn
            >
            <v-btn color="blue darken-1" text @click="associerProfils"
              >Ajouter des profils</v-btn
            >
          </v-card-actions>
        </v-card>
      </v-dialog>
      <!-- /Modal ajouter un profil -->
      <!-- Modal ajouter une collection -->
      <v-dialog
        v-model="dialogCollections"
        max-width="500px"
        persistent
        scrollable
      >
        <v-card>
          <v-card-title>
            <span class="headline">
              <b>Ajouter des dossiers</b>
            </span>
          </v-card-title>
          <v-card-text>
            <v-card class="mx-auto" max-width="800" tile>
              <v-text-field
                v-model="rechercheAjoutsCollections"
                label="Rechercher dans la base de données"
                required
              ></v-text-field>
              <v-data-table
                no-data-text="Aucun élément trouvé"
                no-results-text="Aucun élément trouvé"
                loading-text="Chargement en cours..."
                v-model="selectedAjoutsCollections"
                :headers="headersCollections"
                :items="filteredListCollections"
                :items-per-page="5"
                item-key="id"
                show-select
                class="elevation-1"
              ></v-data-table>
            </v-card>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" text @click="fermerCollections"
              >Retour</v-btn
            >
            <v-btn color="blue darken-1" text @click="associerCollections"
              >Ajouter des dossiers</v-btn
            >
          </v-card-actions>
        </v-card>
      </v-dialog>
      <!-- /Modal ajouter une collection -->
      <!-- Ajouter un element -->
      <v-row v-if="titreClick === true" @click="clickOnTitre()">
        <v-col cols="12">
          <h1 class="text-center">
            {{ titre }}
            <v-btn class="mx-2" fab x-small color="primary">
              <v-icon dark>mdi-pen</v-icon>
            </v-btn>
          </h1>
        </v-col>
      </v-row>
      <v-row v-if="titreClick === false">
        <v-col cols="9">
          <div class="text-center">
            <v-text-field
              v-model="titre"
              placeholder="Ajoutez votre titre ici..."
              autocomplete="nope"
              hint="Modifier le titre de la collection"
            ></v-text-field>
          </div>
        </v-col>
        <v-col cols="3">
          <div class="text-center">
            <div class="my-2" @click="clickOnTitre()">
              <v-btn color="error" dark large>Sauvegarder</v-btn>
            </div>
          </div>
        </v-col>
      </v-row>
      <!-- Ajouter un element -->
      <v-row v-if="commentaireClick === true" @click="clickOnCommentaire()">
        <v-col cols="12">
          <div class="text-center">
            {{ commentaire ? commentaire : "Ajouter un commentaire..." }}
            <v-btn class="mx-2" fab x-small color="primary">
              <v-icon dark>{{ commentaire ? "mdi-pen" : "mdi-plus" }}</v-icon>
            </v-btn>
          </div>
        </v-col>
      </v-row>
      <v-row v-if="commentaireClick === false">
        <v-col cols="9">
          <div class="text-center">
            <v-text-field
              v-model="commentaire"
              placeholder="Ajoutez votre commentaire ici..."
              autocomplete="nope"
              hint="Ajouter un commentaire..."
            ></v-text-field>
          </div>
        </v-col>
        <v-col cols="3">
          <div class="text-center">
            <div class="my-2" @click="clickOnCommentaire()">
              <v-btn color="error" dark large>Sauvegarder</v-btn>
            </div>
          </div>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12">
          <v-btn @click="imprimer" class="mr-3" depressed small color="primary"
            >Imprimer</v-btn
          >
          <v-btn @click="removeCollection" depressed small color="error"
            >Supprimer</v-btn
          >
        </v-col>
      </v-row>
      <br />
      <br />
      <!-- Ajouter un element -->
      <v-row>
        <v-col cols="6" align="start">
          <h2>Association avec les Profils</h2>
        </v-col>
        <v-col cols="6" align="end">
          <v-btn small class="mx-2" color="primary" @click="ajouterProfils"
            >Ajouter un profil</v-btn
          >
          <v-btn
            small
            color="error"
            :disabled="disabledProfils"
            @click="deleteProfils"
            >Supprimer la sélection</v-btn
          >
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
      <br />
      <br />
      <br />
      <!-- /Ajouter un element -->
      <!-- Ajout un element -->
      <v-row>
        <v-col cols="6" align="start">
          <h2>Association avec les Textes</h2>
        </v-col>
        <v-col cols="6" align="end">
          <v-btn small class="mx-2" color="primary" @click="ajouterTextes"
            >Ajouter un texte</v-btn
          >
          <v-btn
            small
            color="error"
            :disabled="disabledTextes"
            @click="deleteTextes"
            >Supprimer la sélection</v-btn
          >
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
      <br />
      <br />
      <br />
      <!-- /Ajout un element -->
      <!-- Ajout un element -->
      <v-row>
        <v-col cols="6" align="start">
          <h2>Association avec les Dossiers</h2>
        </v-col>
        <v-col cols="6" align="end">
          <v-btn small class="mx-2" color="primary" @click="ajouterCollections"
            >Ajouter un dossier</v-btn
          >
          <v-btn
            small
            color="error"
            :disabled="disabledCollections"
            @click="deleteCollections"
            >Supprimer la sélection</v-btn
          >
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="6" align="start">
          <v-text-field
            class="mx-2"
            v-model="searchCollections"
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
        v-model="selectedCollections"
        :headers="headersCollections"
        :items="collections"
        :search="searchCollections"
        item-key="id"
        show-select
        class="elevation-1"
      ></v-data-table>
      <br />
      <br />
      <br />
      <!-- /Ajout un element -->
      <!-- Ajout un element -->
      <v-row>
        <v-col cols="6" align="start">
          <h2>Association avec les Analyses</h2>
        </v-col>
        <v-col cols="6" align="end">
          <v-btn small class="mx-2" color="primary" @click="ajouterTextes"
            >Ajouter une analyse</v-btn
          >
          <v-btn small color="error" :disabled="true"
            >Supprimer la sélection</v-btn
          >
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="6" align="start">
          <v-text-field
            class="mx-2"
            v-model="searchAnalyses"
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
        v-model="selectedCollections"
        :headers="headersAnalyses"
        :items="analyses"
        :search="searchAnalyses"
        item-key="id"
        show-select
        class="elevation-1"
      ></v-data-table>
      <br />
      <br />
      <br />
      <!-- /Ajout un element -->
      <!-- Ajout un element -->
      <v-row>
        <v-col cols="6" align="start">
          <h2>Association avec les Rapports</h2>
        </v-col>
        <v-col cols="6" align="end">
          <v-btn small class="mx-2" color="primary" @click="ajouterTextes"
            >Ajouter un rapport</v-btn
          >
          <v-btn small color="error" :disabled="true"
            >Supprimer la sélection</v-btn
          >
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="6" align="start">
          <v-text-field
            class="mx-2"
            v-model="searchRapports"
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
        v-model="selectedRapports"
        :headers="headersRapports"
        :items="rapports"
        :search="searchRapports"
        item-key="id"
        show-select
        class="elevation-1"
      ></v-data-table>
      <br />
      <br />
      <br />
      <!-- /Ajout un element -->
    </v-container>
  </div>
</template>

<script>
// Importations
import axios from "axios";
import { TabsData } from "../../flux/Tabs";

// Exportations
export default {
  props: {
    content: Object
  },
  data() {
    return {
      // Snackbar
      snackbarAjoute: false,
      snackbarSupprimer: false,
      snackbarModifie: false,
      // Commentaire
      commentaire: "",
      commentaireClick: true,
      // Titre
      titre: "",
      titreClick: true,
      // Desactive
      disabledProfils: true,
      disabledTextes: true,
      disabledCollections: true,
      disabledAnalyses: true,
      disabledRapports: true,
      // Recherche
      searchProfils: "",
      searchTextes: "",
      searchCollections: "",
      searchAnalyses: "",
      searchRapports: "",
      // Selection
      selectedProfils: [],
      selectedTextes: [],
      selectedCollections: [],
      selectedAnalyses: [],
      selectedRapports: [],
      // Headers et contenus
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
      headersCollections: [
        { text: "Titre", value: "titre" },
        { text: "# de textes par l'auteur", value: "nbtextes" },
        { text: "# de mots par l'auteur", value: "nbmots" }
      ],
      collections: [],
      headersAnalyses: [
        { text: "Titre", value: "titre" },
        { text: "Type d'analyse", value: "type" },
        { text: "Ressources de l'auteur", value: "ressources" }
      ],
      analyses: [],
      headersRapports: [
        { text: "Titre", value: "titre" },
        { text: "Type de rapport", value: "type" }
      ],
      rapports: [],
      // Ajouts profils
      dialogProfils: false,
      rechercheAjoutsProfils: "",
      selectedAjoutsProfils: [],
      contentProfils: [],
      // Ajouts textes
      dialogTextes: false,
      rechercheAjoutsTextes: "",
      selectedAjoutsTextes: [],
      contentTextes: [],
      // Ajouts collections
      dialogCollections: false,
      rechercheAjoutsCollections: "",
      selectedAjoutsCollections: [],
      contentCollections: []
    };
  },
  methods: {
    imprimer() {
      // Générer le lien de l'impression
      let imprimer = window.open(
        `${process.env.VUE_APP_SERVEUR}/imprimer-collection/${this.content.id}`,
        "_blank"
      );

      // Traitement du lien
      imprimer.document.close(); //missing code
      imprimer.focus();
      imprimer.print();
    },
    clickOnTitre() {
      this.titreClick = !this.titreClick;
      if (this.titreClick === true) {
        // Appel avec axios
        let formData = new FormData();
        formData.append("id", this.content.id);
        formData.append("commentaire", this.commentaire);
        formData.append("titre", this.titre);
        axios
          .post(process.env.VUE_APP_SERVEUR + "/modifier-collection", formData)
          .then(response => {
            this.snackbarModifie = true;
            console.log(response);
          })
          .catch(error => {
            alert(error);
          });
      }
    },
    clickOnCommentaire() {
      this.commentaireClick = !this.commentaireClick;
      if (this.commentaireClick === true) {
        // Appel avec axios
        let formData = new FormData();
        formData.append("id", this.content.id);
        formData.append("commentaire", this.commentaire);
        formData.append("titre", this.content.titre);
        axios
          .post(process.env.VUE_APP_SERVEUR + "/modifier-collection", formData)
          .then(response => {
            this.snackbarModifie = true;
            console.log(response);
          })
          .catch(error => {
            alert(error);
          });
      }
    },
    removeCollection() {
      if (
        confirm(
          "Voulez-vous vraiment supprimer cette collection et ses analyses définitivement ?"
        )
      ) {
        // Appel avec axios
        let formData = new FormData();
        formData.append("id", this.content.id);
        axios
          .post(process.env.VUE_APP_SERVEUR + "/supprimer-collection", formData)
          .then(response => {
            alert("La collection a bien été supprimée");
            TabsData.remove(TabsData.state.nowId);
            console.log(response);
          })
          .catch(error => {
            alert(error);
          });
      }
    },
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
    ajouterTextes() {
      let formData = new FormData();
      formData.append("req", "");
      axios
        .post(process.env.VUE_APP_SERVEUR + "/searchtextes", formData)
        .then(response => {
          console.log("reponse :", response.data);
          this.contentTextes = response.data;
        })
        .catch(e => {
          this.getError = true;
          console.error("Impossible de charger les données", e);
        });
      this.dialogTextes = !this.dialogTextes;
      console.log("Ok");
    },
    ajouterCollections() {
      let formData = new FormData();
      formData.append("req", "");
      axios
        .post(process.env.VUE_APP_SERVEUR + "/search-dossier", formData)
        .then(response => {
          console.log("reponse :", response.data);
          this.contentCollections = response.data;
        })
        .catch(e => {
          this.getError = true;
          console.error("Impossible de charger les données", e);
        });
      this.dialogCollections = !this.dialogCollections;
      console.log("Ok");
    },
    associerProfils() {
      if (confirm("Voulez-vous vraiment ajouter cette association ?")) {
        let formData = new FormData();
        this.selectedAjoutsProfils.map(e => {
          formData = new FormData();
          formData.append("champs1", "Collection");
          formData.append("champs2", "Profil");
          formData.append("idchamps1", this.content.id);
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
              newFormData.append("id", this.content.id);
              newFormData.append("type", "Collection");
              newFormData.append("get", "Profil");

              // Appel avec axios
              axios
                .post(process.env.VUE_APP_SERVEUR + "/assoc", newFormData)
                .then(response => {
                  let result = JSON.parse(response.data);
                  this.profils = result;
                  this.snackbarAjoute = true;
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
    associerTextes() {
      if (confirm("Voulez-vous vraiment ajouter cette association ?")) {
        let formData = new FormData();
        this.selectedAjoutsTextes.map(e => {
          formData = new FormData();
          formData.append("champs1", "Collection");
          formData.append("champs2", "Texte");
          formData.append("idchamps1", this.content.id);
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
              newFormData.append("id", this.content.id);
              newFormData.append("type", "Collection");
              newFormData.append("get", "Texte");

              // Appel avec axios
              axios
                .post(process.env.VUE_APP_SERVEUR + "/assoc", newFormData)
                .then(response => {
                  let result = JSON.parse(response.data);
                  this.textes = result;
                  this.snackbarAjoute = true;
                })
                .catch(error => {
                  this.textes = [];
                  this.snackbarAjoute = true;
                  console.log(error);
                });
              // /TypeProfils
            })
            .catch(error => {
              console.log(error);
            });
        });
        this.selectedAjoutsTextes = [];
        this.dialogTextes = false;
      }
    },
    associerCollections() {
      if (confirm("Voulez-vous vraiment ajouter cette association ?")) {
        let formData = new FormData();
        this.selectedAjoutsCollections.map(e => {
          formData = new FormData();
          formData.append("champs1", "Collection");
          formData.append("champs2", "Dossier");
          formData.append("idchamps1", this.content.id);
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
              newFormData.append("id", this.content.id);
              newFormData.append("type", "Collection");
              newFormData.append("get", "Dossier");

              // Appel avec axios
              axios
                .post(process.env.VUE_APP_SERVEUR + "/assoc", newFormData)
                .then(response => {
                  let result = JSON.parse(response.data);
                  this.collections = result;
                  this.snackbarAjoute = true;
                })
                .catch(error => {
                  this.collections = [];
                  this.snackbarAjoute = true;
                  console.error(error);
                });
              // /TypeProfils
            })
            .catch(error => {
              console.error(error);
            });
        });
        this.selectedAjoutsCollections = [];
        this.dialogCollections = false;
      }
    },
    fermerCollections() {
      this.dialogCollections = false;
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
              newFormData.append("id", this.content.id);
              newFormData.append("type", "Collection");
              newFormData.append("get", "Profil");

              // Appel avec axios
              axios
                .post(process.env.VUE_APP_SERVEUR + "/assoc", newFormData)
                .then(response => {
                  let result = JSON.parse(response.data);
                  this.profils = result;
                  this.snackbarSupprimer = true;
                })
                .catch(error => {
                  this.profils = [];
                  this.snackbarSupprimer = true;
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
    },
    deleteCollections() {
      if (confirm("Voulez-vous vraiment supprimer cette association ?")) {
        let formData = new FormData();
        this.selectedCollections.map(e => {
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
              newFormData.append("id", this.content.id);
              newFormData.append("type", "Collection");
              newFormData.append("get", "Dossier");

              // Appel avec axios
              axios
                .post(process.env.VUE_APP_SERVEUR + "/assoc", newFormData)
                .then(response => {
                  let result = JSON.parse(response.data);
                  this.collections = result;
                  this.snackbarSupprimer = true;
                })
                .catch(error => {
                  this.collections = [];
                  this.snackbarSupprimer = true;
                  console.log(error);
                });
              // /TypeProfils
            })
            .catch(error => {
              console.log(error);
            });
        });
        this.selectedCollections = [];
      }
    },
    deleteTextes() {
      if (confirm("Voulez-vous vraiment supprimer cette association ?")) {
        let formData = new FormData();
        this.selectedTextes.map(e => {
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
              newFormData.append("id", this.content.id);
              newFormData.append("type", "Collection");
              newFormData.append("get", "Texte");

              // Appel avec axios
              axios
                .post(process.env.VUE_APP_SERVEUR + "/assoc", newFormData)
                .then(response => {
                  let result = JSON.parse(response.data);
                  this.textes = result;
                  this.snackbarSupprimer = true;
                })
                .catch(error => {
                  this.textes = [];
                  this.snackbarSupprimer = true;
                  console.log(error);
                });
              // /TypeProfils
            })
            .catch(error => {
              console.log(error);
            });
        });
        this.selectedTextes = [];
      }
    }
  },
  mounted: function() {
    // TypeProfils
    // Ajout en formulaire
    let formData = new FormData();
    formData.append("id", this.content.id);
    formData.append("type", "Collection");
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
    formData.append("id", this.content.id);
    formData.append("type", "Collection");
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

    // TypeCollections
    // Ajout en formulaire
    formData = new FormData();
    formData.append("id", this.content.id);
    formData.append("type", "Collection");
    formData.append("get", "Dossier");

    // Appel avec axios
    axios
      .post(process.env.VUE_APP_SERVEUR + "/assoc", formData)
      .then(response => {
        let result = JSON.parse(response.data);
        this.collections = result;
      })
      .catch(error => {
        console.log(error);
      });
    // /TypeCollections
    // Commentaire
    // Appel avec axios
    formData = new FormData();
    formData.append("req", this.content.id);
    axios
      .post(process.env.VUE_APP_SERVEUR + "/search-collection", formData)
      .then(response => {
        this.commentaire = response.data[0].commentaire;
        if (this.commentaire == "None") {
          this.commentaire = "";
        }
      })
      .catch(error => {
        console.log(error);
      });

    // Ajout du titre en variable
    this.titre = this.content.titre;
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

    // Collections
    if (this.selectedCollections.length > 0) {
      this.disabledCollections = false;
    } else {
      this.disabledCollections = true;
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
    },
    filteredListTextes() {
      return this.contentTextes.filter(p => {
        return p.titre
          .toLowerCase()
          .includes(this.rechercheAjoutsTextes.toLowerCase());
      });
    },
    filteredListCollections() {
      return this.contentCollections.filter(p => {
        return p.titre
          .toLowerCase()
          .includes(this.rechercheAjoutsCollections.toLowerCase());
      });
    }
  }
};
</script>
