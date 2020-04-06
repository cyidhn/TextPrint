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
        Les éléments ont bien été retirés de la liste.
        <v-btn dark text @click="snackbarSupprimer = false">Fermer</v-btn>
      </v-snackbar>
      <!-- /Snackbar Supprimé avec succès -->
      <!-- Modal global -->
      <v-dialog v-model="dialogGlobal" max-width="1200px" persistent scrollable>
        <v-card>
          <v-card-title>
            <span class="headline">
              <b>Associer ces éléments au dossier</b>
            </span>
          </v-card-title>
          <v-card-text>
            <v-card class="mx-auto" max-width="1200" tile>
              <v-container fluid>
                <v-text-field
                  v-model="searchGlobal"
                  label="Rechercher dans la base de données"
                  required
                ></v-text-field>
                <v-row>
                  <v-col cols="6">
                    <h2 class="mt-8 mb-6"><b>Séléctionner des éléments</b></h2>
                    <v-data-table
                      no-data-text="Aucun élément trouvé"
                      no-results-text="Aucun élément trouvé"
                      loading-text="Chargement en cours..."
                      v-model="selectedAjoutsGlobal"
                      :headers="headersGlobal"
                      :items="contentGlobal"
                      :search="searchGlobal"
                      :items-per-page="5"
                      item-key="id"
                      show-select
                      class="elevation-1"
                    ></v-data-table>
                  </v-col>
                  <v-col cols="6">
                    <h2 class="mt-8 mb-6"><b>Éléments ajouté au dossier</b></h2>
                    <v-data-table
                      no-data-text="Aucun élément ajouté"
                      no-results-text="Aucun élément trouvé"
                      loading-text="Chargement en cours..."
                      v-model="selectedAjoutsGlobal"
                      :headers="headersGlobal"
                      :items="selectedAjoutsGlobal"
                      :search="searchGlobal"
                      :items-per-page="5"
                      item-key="id"
                      show-select
                      class="elevation-1"
                    ></v-data-table>
                  </v-col>
                </v-row>
              </v-container>
            </v-card>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" text @click="fermerGlobal"
              >Retour</v-btn
            >
            <v-btn color="blue darken-1" text @click="addElementToGlobal"
              >Ajouter</v-btn
            >
          </v-card-actions>
        </v-card>
      </v-dialog>
      <!-- /Modal global -->
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
            <v-btn color="blue darken-1" text @click="fermerTextes"
              >Retour</v-btn
            >
            <v-btn color="blue darken-1" text @click="nouveauTexte"
              >Nouveau</v-btn
            >
            <v-btn color="blue darken-1" text @click="associerTextes"
              >Ajouter</v-btn
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
            <v-btn color="blue darken-1" text @click="fermerProfils"
              >Retour</v-btn
            >
            <v-btn color="blue darken-1" text @click="nouveauProfil"
              >Nouveau</v-btn
            >
            <v-btn color="blue darken-1" text @click="associerProfils"
              >Ajouter</v-btn
            >
          </v-card-actions>
        </v-card>
      </v-dialog>
      <!-- /Modal ajouter un profil -->
      <!-- Modal ajouter une collection -->
      <v-dialog
        v-model="dialogCollections"
        max-width="800px"
        persistent
        scrollable
      >
        <v-card>
          <v-card-title>
            <span class="headline">
              <b>Ajouter des collections</b>
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
            <v-btn color="blue darken-1" text @click="nouvelleCollection"
              >Nouveau</v-btn
            >
            <v-btn color="blue darken-1" text @click="associerCollections"
              >Ajouter</v-btn
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
              hint="Modifier le titre du dossier"
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
          <v-btn @click="removeDossier" depressed small color="error"
            >Supprimer</v-btn
          >
        </v-col>
      </v-row>
      <br />
      <br />
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
            >Supprimer de la liste</v-btn
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
        :loading="loadingProfils"
        v-model="selectedProfils"
        :headers="headersProfils"
        :items="profils"
        :search="searchProfils"
        item-key="id"
        show-select
        class="elevation-1"
      >
        <!-- Template view -->
        <template v-slot:item.actions="{ item }">
          <v-icon small class="ml-1" @click="viewItem(item)">
            mdi-eye
          </v-icon>
        </template>
      </v-data-table>
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
            >Supprimer de la liste</v-btn
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
        :loading="loadingTextes"
        v-model="selectedTextes"
        :headers="headersTextes"
        :items="textes"
        :search="searchTextes"
        item-key="id"
        show-select
        class="elevation-1"
      >
        <!-- Template view -->
        <template v-slot:item.actions="{ item }">
          <v-icon small class="ml-1" @click="viewItem(item)">
            mdi-eye
          </v-icon>
        </template>
      </v-data-table>
      <br />
      <br />
      <br />
      <!-- /Ajout un element -->
      <!-- Ajout un element -->
      <v-row>
        <v-col cols="6" align="start">
          <h2>Association avec les Collections</h2>
        </v-col>
        <v-col cols="6" align="end">
          <v-btn small class="mx-2" color="primary" @click="ajouterCollections"
            >Ajouter une collection</v-btn
          >
          <v-btn
            small
            color="error"
            :disabled="disabledCollections"
            @click="deleteCollections"
            >Supprimer de la liste</v-btn
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
        :loading="loadingTextes"
        v-model="selectedCollections"
        :headers="headersCollections"
        :items="collections"
        :search="searchCollections"
        item-key="id"
        show-select
        class="elevation-1"
      >
        <!-- Template view -->
        <template v-slot:item.actions="{ item }">
          <v-icon small class="ml-1" @click="viewItem(item)">
            mdi-eye
          </v-icon>
        </template>
      </v-data-table>
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
            >Supprimer de la liste</v-btn
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
            >Supprimer de la liste</v-btn
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
import { AddData } from "../../flux/Add";
import { DialogsData } from "../../flux/Dialogs";

// Exportation de la fonction
export default {
  props: {
    content: Object,
  },
  data() {
    return {
      selectedAjoutsGlobal: [],
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
      searchGlobal: "",
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
        { text: "Prénom NOM", value: "nom" },
        { text: "Voir", value: "actions", sortable: false },
      ],
      profils: [],
      headersTextes: [
        { text: "Titre", value: "titre" },
        { text: "# Versions", value: "version" },
        { text: "Voir", value: "actions", sortable: false },
      ],
      textes: [],
      headersCollections: [
        { text: "Titre", value: "titre" },
        { text: "# de textes par l'auteur", value: "nbtextes" },
        { text: "# de mots par l'auteur", value: "nbmots" },
        { text: "Voir", value: "actions", sortable: false },
      ],
      collections: [],
      headersAnalyses: [
        { text: "Titre", value: "titre" },
        { text: "Type d'analyse", value: "type" },
        { text: "Ressources de l'auteur", value: "ressources" },
      ],
      analyses: [],
      headersRapports: [
        { text: "Titre", value: "titre" },
        { text: "Type de rapport", value: "type" },
      ],
      rapports: [],
      headersGlobal: [
        { text: "Type", value: "type" },
        { text: "Titre", value: "titre" },
        { text: "Alias", value: "alias" },
        { text: "Prénom", value: "prenom" },
        { text: "Nom", value: "nom" },
      ],
      contentGlobal: [],
      // Ajouts profils
      dialogProfils: false,
      rechercheAjoutsProfils: "",
      selectedAjoutsProfils: [],
      contentProfils: [],
      loadingProfils: true,
      // Ajouts textes
      dialogTextes: false,
      rechercheAjoutsTextes: "",
      selectedAjoutsTextes: [],
      contentTextes: [],
      loadingTextes: true,
      // Ajouts collections
      dialogCollections: false,
      rechercheAjoutsCollections: "",
      selectedAjoutsCollections: [],
      contentCollections: [],
      loadingCollections: true,
      // Ajout Global
      dialogGlobal: false,
    };
  },
  methods: {
    viewItem(item) {
      let formData = new FormData();
      // Pour les profils
      if (item.type == "Profil connu" || item.type == "Profil anonyme") {
        formData = new FormData();
        formData.append("req", item.cle_id);
        // Appel avec axios
        axios
          .post(process.env.VUE_APP_SERVEUR + "/search-profil", formData)
          .then((response) => {
            console.log(response.data);
            TabsData.add(item.alias + " " + item.nom, response.data[0]);
          })
          .catch((error) => {
            console.log(error);
          });
      }
      // Pour les textes
      if (item.type == "Texte") {
        formData = new FormData();
        formData.append("req", item.cle_id);
        // Appel avec axios
        axios
          .post(process.env.VUE_APP_SERVEUR + "/search-texte", formData)
          .then((response) => {
            console.log(response.data);
            TabsData.add(item.titre, response.data[0]);
          })
          .catch((error) => {
            console.log(error);
          });
      }
      // Pour les collections
      if (item.type == "Collection") {
        formData = new FormData();
        formData.append("req", item.cle_id);
        // Appel avec axios
        axios
          .post(process.env.VUE_APP_SERVEUR + "/search-collection", formData)
          .then((response) => {
            console.log(response.data);
            TabsData.add(item.titre, response.data[0]);
          })
          .catch((error) => {
            console.log(error);
          });
      }
      // Pour les dossiers
      if (item.type == "Dossier") {
        formData = new FormData();
        formData.append("req", item.cle_id);
        // Appel avec axios
        axios
          .post(process.env.VUE_APP_SERVEUR + "/search-dossier", formData)
          .then((response) => {
            console.log(response.data);
            TabsData.add(item.titre, response.data[0]);
          })
          .catch((error) => {
            console.log(error);
          });
      }
      console.log(item);
    },
    addElementToGlobal() {
      if (confirm("Voulez-vous ajouter cette sélection à votre dossier ?")) {
        let formData = new FormData();
        this.selectedAjoutsGlobal.map((e) => {
          if (e.type == "Dossiers") {
            e.type = "Dossier";
          }
          if (e.type == "Collections") {
            e.type = "Collection";
          }
          formData = new FormData();
          formData.append("champs1", "Dossier");
          formData.append("champs2", e.type);
          formData.append("idchamps1", this.content.id);
          formData.append("idchamps2", e.id);
          // Appel avec axios
          axios
            .post(
              process.env.VUE_APP_SERVEUR + "/associer-generalement",
              formData
            )
            .then((response) => {
              console.log(response.data);
              this.majDossier();
            })
            .catch((error) => {
              console.log(error);
            });
        });
        this.selectedAjoutsGlobal = [];
        AddData.close();
        this.dialogGlobal = false;
      }
    },
    shuffleContent(a) {
      var j, x, i;
      for (i = a.length - 1; i > 0; i--) {
        j = Math.floor(Math.random() * (i + 1));
        x = a[i];
        a[i] = a[j];
        a[j] = x;
      }
      return a;
    },
    updateContent() {
      axios
        .get(process.env.VUE_APP_SERVEUR + "/test")
        .then((response) => {
          this.contentGlobal = response.data;
          this.contentGlobal = this.shuffleContent(this.contentGlobal);
          this.contentGlobal = this.suppressionFolder(
            this.contentGlobal,
            "Dossiers"
          );
        })
        .catch((e) => {
          this.getError = true;
          console.error("Impossible de charger les données", e);
        });
    },
    fermerGlobal() {
      AddData.close();
      this.dialogGlobal = false;
    },
    associerGlobal() {
      console.log("Associer globalement");
    },
    nouveauTexte() {
      DialogsData.open("texte");
      DialogsData.addToFolder("Dossier", this.content.id);
    },
    nouveauProfil() {
      DialogsData.open("profil-connu");
      DialogsData.addToFolder("Dossier", this.content.id);
    },
    nouvelleCollection() {
      DialogsData.open("collection");
      DialogsData.addToFolder("Dossier", this.content.id);
    },
    imprimer() {
      // Générer le lien de l'impression
      let imprimer = window.open(
        `${process.env.VUE_APP_SERVEUR}/imprimer-dossier/${this.content.id}`,
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
          .post(process.env.VUE_APP_SERVEUR + "/modifier-dossier", formData)
          .then((response) => {
            this.snackbarModifie = true;
            TabsData.changeName(TabsData.state.nowId, this.titre);
            this.content.titre = this.titre;
            console.log(response);
          })
          .catch((error) => {
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
        formData.append("titre", this.titre);
        axios
          .post(process.env.VUE_APP_SERVEUR + "/modifier-dossier", formData)
          .then((response) => {
            this.snackbarModifie = true;
            console.log(response);
          })
          .catch((error) => {
            alert(error);
          });
      }
    },
    removeDossier() {
      if (
        confirm(
          "Voulez-vous vraiment supprimer ce dossier et ses analyses définitivement ?"
        )
      ) {
        // Appel avec axios
        let formData = new FormData();
        formData.append("id", this.content.id);
        axios
          .post(process.env.VUE_APP_SERVEUR + "/supprimer-dossier", formData)
          .then((response) => {
            alert("Le dossier a bien été supprimé");
            TabsData.remove(TabsData.state.nowId);
            console.log(response);
          })
          .catch((error) => {
            alert(error);
          });
      }
    },
    ajouterProfils() {
      let formData = new FormData();
      formData.append("req", "");
      axios
        .post(process.env.VUE_APP_SERVEUR + "/searchprofil", formData)
        .then((response) => {
          this.contentProfils = response.data;
          // Suppression du doublon
          this.contentProfils = this.suppressionDoublon(
            this.profils,
            this.contentProfils
          );
          // /Suppression du doublon
        })
        .catch((e) => {
          this.getError = true;
          console.error("Impossible de charger les données", e);
        });
      this.dialogProfils = !this.dialogProfils;
      console.log("Ok");
    },
    suppressionDoublon(texte, contentTexte) {
      // Suppression du doublon
      for (let i = 0; i < texte.length; i++) {
        for (let l = 0; l < contentTexte.length; l++) {
          if (texte[i].cle_id == contentTexte[l].id) {
            contentTexte.splice(l, 1);
            l--;
          }
        }
      }
      // /Suppression du doublon
      return contentTexte;
    },
    suppressionFolder(texte, type) {
      // Suppression du doublon
      for (let i = 0; i < texte.length; i++) {
        if (texte[i].type == type) {
          texte.splice(i, 1);
          i--;
        }
      }
      // /Suppression du doublon
      return texte;
    },
    ajouterTextes() {
      let formData = new FormData();
      formData.append("req", "");
      axios
        .post(process.env.VUE_APP_SERVEUR + "/searchtextes", formData)
        .then((response) => {
          this.contentTextes = response.data;
          this.contentTextes = this.suppressionDoublon(
            this.textes,
            this.contentTextes
          );
          // // Suppression du doublon
          // for (let i = 0; i < this.textes.length; i++) {
          //   for (let l = 0; l < this.contentTextes.length; l++) {
          //     if (this.textes[i].cle_id == this.contentTextes[l].id) {
          //       this.contentTextes.splice(l, 1);
          //       l--;
          //     }
          //   }
          // }
          // // /Suppression du doublon
        })
        .catch((e) => {
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
        .post(process.env.VUE_APP_SERVEUR + "/searchcollections", formData)
        .then((response) => {
          console.log("reponse :", response.data);
          this.contentCollections = response.data;
          // Suppression du doublon
          this.contentCollections = this.suppressionDoublon(
            this.collections,
            this.contentCollections
          );
          // /Suppression du doublon
        })
        .catch((e) => {
          this.getError = true;
          console.error("Impossible de charger les données", e);
        });
      this.dialogCollections = !this.dialogCollections;
      console.log("Ok");
    },
    associerProfils() {
      if (confirm("Voulez-vous vraiment ajouter cette association ?")) {
        let formData = new FormData();
        this.selectedAjoutsProfils.map((e) => {
          formData = new FormData();
          formData.append("champs1", "Dossier");
          formData.append("champs2", "Profil");
          formData.append("idchamps1", this.content.id);
          formData.append("idchamps2", e.id);
          // Appel avec axios
          axios
            .post(
              process.env.VUE_APP_SERVEUR + "/associer-generalement",
              formData
            )
            .then((response) => {
              console.log(response.data);
              // TypeProfils
              // Ajout en formulaire
              let newFormData = new FormData();
              newFormData.append("id", this.content.id);
              newFormData.append("type", "Dossier");
              newFormData.append("get", "Profil");

              // Appel avec axios
              axios
                .post(process.env.VUE_APP_SERVEUR + "/assoc", newFormData)
                .then((response) => {
                  let result = JSON.parse(response.data);
                  this.profils = result;
                  this.snackbarAjoute = true;
                })
                .catch((error) => {
                  this.profils = [];
                  console.log(error);
                });
              // /TypeProfils
            })
            .catch((error) => {
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
        this.selectedAjoutsTextes.map((e) => {
          formData = new FormData();
          formData.append("champs1", "Dossier");
          formData.append("champs2", "Texte");
          formData.append("idchamps1", this.content.id);
          formData.append("idchamps2", e.id);
          // Appel avec axios
          axios
            .post(
              process.env.VUE_APP_SERVEUR + "/associer-generalement",
              formData
            )
            .then((response) => {
              console.log(response.data);
              // TypeProfils
              // Ajout en formulaire
              let newFormData = new FormData();
              newFormData.append("id", this.content.id);
              newFormData.append("type", "Dossier");
              newFormData.append("get", "Texte");

              // Appel avec axios
              axios
                .post(process.env.VUE_APP_SERVEUR + "/assoc", newFormData)
                .then((response) => {
                  let result = JSON.parse(response.data);
                  this.textes = result;
                  this.snackbarAjoute = true;
                })
                .catch((error) => {
                  this.textes = [];
                  this.snackbarAjoute = true;
                  console.log(error);
                });
              // /TypeProfils
            })
            .catch((error) => {
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
        this.selectedAjoutsCollections.map((e) => {
          formData = new FormData();
          formData.append("champs1", "Dossier");
          formData.append("champs2", "Collection");
          formData.append("idchamps1", this.content.id);
          formData.append("idchamps2", e.id);
          // Appel avec axios
          axios
            .post(
              process.env.VUE_APP_SERVEUR + "/associer-generalement",
              formData
            )
            .then((response) => {
              console.log(response.data);
              // TypeProfils
              // Ajout en formulaire
              let newFormData = new FormData();
              newFormData.append("id", this.content.id);
              newFormData.append("type", "Dossier");
              newFormData.append("get", "Collection");

              // Appel avec axios
              axios
                .post(process.env.VUE_APP_SERVEUR + "/assoc", newFormData)
                .then((response) => {
                  let result = JSON.parse(response.data);
                  this.collections = result;
                  this.snackbarAjoute = true;
                })
                .catch((error) => {
                  // En cas d'erreur
                  this.collections = [];
                  this.snackbarAjoute = true;
                  console.error(error);
                });
              // /TypeProfils
            })
            .catch((error) => {
              console.error(error);
            });
        });
        this.selectedAjoutsCollections = [];
        this.dialogCollections = false;
      }
    },
    fermerCollections() {
      DialogsData.init();
      this.majDossier();
      this.dialogCollections = false;
    },
    fermerProfils() {
      DialogsData.init();
      this.majDossier();
      this.dialogProfils = false;
    },
    fermerTextes() {
      DialogsData.init();
      this.majDossier();
      this.dialogTextes = false;
    },
    deleteProfils() {
      // Message de suppression de profil
      if (confirm("Voulez-vous retirer la sélection de cette liste ?")) {
        let formData = new FormData();
        this.selectedProfils.map((e) => {
          formData = new FormData();
          formData.append("id", e.delete);
          // Appel avec axios
          axios
            .post(
              process.env.VUE_APP_SERVEUR + "/supprimer-association",
              formData
            )
            .then((response) => {
              console.log(response);
              // TypeProfils
              // Ajout en formulaire
              let newFormData = new FormData();
              newFormData.append("id", this.content.id);
              newFormData.append("type", "Dossier");
              newFormData.append("get", "Profil");

              // Appel avec axios
              axios
                .post(process.env.VUE_APP_SERVEUR + "/assoc", newFormData)
                .then((response) => {
                  let result = JSON.parse(response.data);
                  this.profils = result;
                  this.snackbarSupprimer = true;
                  this.majDossier();
                })
                .catch((error) => {
                  this.profils = [];
                  this.snackbarSupprimer = true;
                  console.log(error);
                });
              // /TypeProfils
            })
            .catch((error) => {
              console.log(error);
            });
        });
        this.selectedProfils = [];
      }
    },
    deleteCollections() {
      if (confirm("Voulez-vous retirer la sélection de cette liste ?")) {
        let formData = new FormData();
        this.selectedCollections.map((e) => {
          formData = new FormData();
          formData.append("id", e.delete);
          // Appel avec axios
          axios
            .post(
              process.env.VUE_APP_SERVEUR + "/supprimer-association",
              formData
            )
            .then((response) => {
              console.log(response);
              // TypeProfils
              // Ajout en formulaire
              let newFormData = new FormData();
              newFormData.append("id", this.content.id);
              newFormData.append("type", "Dossier");
              newFormData.append("get", "Collection");

              // Appel avec axios
              axios
                .post(process.env.VUE_APP_SERVEUR + "/assoc", newFormData)
                .then((response) => {
                  let result = JSON.parse(response.data);
                  this.collections = result;
                  this.snackbarSupprimer = true;
                })
                .catch((error) => {
                  this.collections = [];
                  this.snackbarSupprimer = true;
                  console.log(error);
                });
              // /TypeProfils
            })
            .catch((error) => {
              console.log(error);
            });
        });
        this.selectedCollections = [];
      }
    },
    majDossier() {
      // TypeProfils
      // Ajout en formulaire
      let formData = new FormData();
      formData.append("id", this.content.id);
      formData.append("type", "Dossier");
      formData.append("get", "Profil");

      // Appel avec axios
      axios
        .post(process.env.VUE_APP_SERVEUR + "/assoc", formData)
        .then((response) => {
          let result = JSON.parse(response.data);
          // Traitement
          for (let i = 0; i < result.length; i++) {
            if (result[i].alias == "undefined") {
              result[i].alias = "";
            }
            if (result[i].prenom == "undefined") {
              result[i].prenom = "";
            }
            if (result[i].nom == "undefined undefined") {
              result[i].nom = "";
            }
          }
          this.profils = result;
          this.loadingProfils = false;
        })
        .catch((error) => {
          console.log(error);
          this.loadingProfils = false;
        });
      // /TypeProfils

      // TypeTextes
      // Ajout en formulaire
      formData = new FormData();
      formData.append("id", this.content.id);
      formData.append("type", "Dossier");
      formData.append("get", "Texte");

      // Appel avec axios
      axios
        .post(process.env.VUE_APP_SERVEUR + "/assoc", formData)
        .then((response) => {
          let result = JSON.parse(response.data);
          this.textes = result;
          this.loadingTextes = false;
        })
        .catch((error) => {
          console.log(error);
          this.loadingTextes = false;
        });
      // /TypeTextes

      // TypeCollections
      // Ajout en formulaire
      formData = new FormData();
      formData.append("id", this.content.id);
      formData.append("type", "Dossier");
      formData.append("get", "Collection");

      // Appel avec axios
      axios
        .post(process.env.VUE_APP_SERVEUR + "/assoc", formData)
        .then((response) => {
          let result = JSON.parse(response.data);
          this.collections = result;
          this.loadingCollections = false;
        })
        .catch((error) => {
          console.log(error);
          this.loadingCollections = false;
        });
      // /TypeCollection

      // Commentaire
      // Appel avec axios
      formData = new FormData();
      formData.append("req", this.content.id);
      axios
        .post(process.env.VUE_APP_SERVEUR + "/search-dossier", formData)
        .then((response) => {
          this.commentaire = response.data[0].commentaire;
          if (this.commentaire == "None") {
            this.commentaire = "";
          }
        })
        .catch((error) => {
          console.log(error);
        });

      // Ajout du titre en variable
      this.titre = this.content.titre;
    },
    deleteTextes() {
      if (confirm("Voulez-vous retirer la sélection de cette liste ?")) {
        let formData = new FormData();
        this.selectedTextes.map((e) => {
          formData = new FormData();
          formData.append("id", e.delete);
          // Appel avec axios
          axios
            .post(
              process.env.VUE_APP_SERVEUR + "/supprimer-association",
              formData
            )
            .then((response) => {
              console.log(response);
              // TypeProfils
              // Ajout en formulaire
              let newFormData = new FormData();
              newFormData.append("id", this.content.id);
              newFormData.append("type", "Dossier");
              newFormData.append("get", "Texte");

              // Appel avec axios
              axios
                .post(process.env.VUE_APP_SERVEUR + "/assoc", newFormData)
                .then((response) => {
                  let result = JSON.parse(response.data);
                  this.textes = result;
                  this.snackbarSupprimer = true;
                })
                .catch((error) => {
                  this.textes = [];
                  this.snackbarSupprimer = true;
                  console.log(error);
                });
              // /TypeProfils
            })
            .catch((error) => {
              console.log(error);
            });
        });
        this.selectedTextes = [];
      }
    },
  },
  mounted: function () {
    // TypeProfils
    // Ajout en formulaire
    let formData = new FormData();
    formData.append("id", this.content.id);
    formData.append("type", "Dossier");
    formData.append("get", "Profil");

    // Appel avec axios
    axios
      .post(process.env.VUE_APP_SERVEUR + "/assoc", formData)
      .then((response) => {
        let result = JSON.parse(response.data);
        // Traitement
        for (let i = 0; i < result.length; i++) {
          if (result[i].alias == "undefined") {
            result[i].alias = "";
          }
          if (result[i].prenom == "undefined") {
            result[i].prenom = "";
          }
          if (result[i].nom == "undefined undefined") {
            result[i].nom = "";
          }
        }
        this.profils = result;
        // /Traitement
        this.loadingProfils = false;
      })
      .catch((error) => {
        console.log(error);
        this.loadingProfils = false;
      });
    // /TypeProfils

    // TypeTextes
    // Ajout en formulaire
    formData = new FormData();
    formData.append("id", this.content.id);
    formData.append("type", "Dossier");
    formData.append("get", "Texte");

    // Appel avec axios
    axios
      .post(process.env.VUE_APP_SERVEUR + "/assoc", formData)
      .then((response) => {
        let result = JSON.parse(response.data);
        this.textes = result;
        this.loadingTextes = false;
      })
      .catch((error) => {
        console.log(error);
        this.loadingTextes = false;
      });
    // /TypeTextes

    // TypeCollections
    // Ajout en formulaire
    formData = new FormData();
    formData.append("id", this.content.id);
    formData.append("type", "Dossier");
    formData.append("get", "Collection");

    // Appel avec axios
    axios
      .post(process.env.VUE_APP_SERVEUR + "/assoc", formData)
      .then((response) => {
        let result = JSON.parse(response.data);
        this.collections = result;
        this.loadingCollections = false;
      })
      .catch((error) => {
        console.log(error);
        this.loadingCollections = false;
      });
    // /TypeCollection

    // Commentaire
    // Appel avec axios
    formData = new FormData();
    formData.append("req", this.content.id);
    axios
      .post(process.env.VUE_APP_SERVEUR + "/search-dossier", formData)
      .then((response) => {
        this.commentaire = response.data[0].commentaire;
        if (this.commentaire == "None") {
          this.commentaire = "";
        }
      })
      .catch((error) => {
        console.log(error);
      });

    // Si la fenetre est ouverte
    if (AddData.state.openWindow) {
      this.dialogGlobal = true;
      this.updateContent();
    }

    // Ajout du titre en variable
    this.titre = this.content.titre;
  },
  updated: function () {
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
      return this.contentProfils.filter((p) => {
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
      return this.contentTextes.filter((p) => {
        return p.titre
          .toLowerCase()
          .includes(this.rechercheAjoutsTextes.toLowerCase());
      });
    },
    filteredListCollections() {
      return this.contentCollections.filter((p) => {
        return p.titre
          .toLowerCase()
          .includes(this.rechercheAjoutsCollections.toLowerCase());
      });
    },
  },
};
</script>
