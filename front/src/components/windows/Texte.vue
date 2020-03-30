<template>
  <div>
    <v-container>
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
      <!-- Modal ajouter un profil -->
      <v-dialog v-model="dialogProfils" max-width="800px" persistent scrollable>
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
                :headers="headersProfilsT"
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
              >Nouveau profil</v-btn
            >
            <v-btn color="blue darken-1" text @click="associerProfils"
              >Ajouter des profils</v-btn
            >
          </v-card-actions>
        </v-card>
      </v-dialog>
      <!-- /Modal ajouter un profil -->
      <v-row>
        <v-col cols="12">
          <v-btn
            @click="ajouterProfils"
            class="mr-3"
            depressed
            small
            color="primary"
            >Associer un profil</v-btn
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
      <!-- Affichage profils -->
      <hr class="mt-8 mb-8" />
      <v-row>
        <v-col cols="6" align="start">
          <h2>Profils</h2>
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
        :loading="loadingProfils"
        v-model="selectedProfils"
        :headers="headersProfils"
        :items="profils"
        :search="searchProfils"
        item-key="id"
        show-select
        class="elevation-1"
      ></v-data-table>
      <hr class="mt-8 mb-8" />
      <!-- /Affichage profils -->
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
            :disabled="true"
            v-model="content.typeDocument1"
            label="Type de document*"
            @change="changeForm()"
            required
          ></v-select>
          <v-select
            :items="[content.typeDocument2]"
            :disabled="true"
            v-model="content.typeDocument2"
            @change="changeForm()"
            required
          ></v-select>
          <v-text-field
            v-model="content.typeDocument3"
            :disabled="true"
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
            :disabled="true"
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
          <v-btn block color="error" class="mt-4" @click="sauvegarder"
            >Sauvegarder</v-btn
          >
        </v-col>
      </v-row>
      <!-- Versions -->
      <hr class="mt-8 mb-8" />
      <v-row>
        <v-col cols="6" align="start">
          <h2>Versions</h2>
        </v-col>
        <!-- <v-col cols="6" align="end">
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
        </v-col> -->
      </v-row>
      <v-row>
        <v-col cols="12" align="start">
          <v-text-field
            class="mx-2"
            v-model="searchVersions"
            label="Filtrer"
            single-line
            hide-details
          ></v-text-field>
        </v-col>
      </v-row>
      <br />
      <v-data-table
        no-data-text="Aucune version de texte trouvée"
        no-results-text="Aucune version de texte trouvée"
        loading-text="Chargement en cours..."
        :headers="headersVersions"
        :items="versions"
        :search="searchVersions"
        item-key="id"
        show-select
        class="elevation-1"
      ></v-data-table>
      <hr class="mt-8 mb-8" />
      <!-- /Ajout un element -->
      <!-- /Versions -->
      <!-- Collections -->
      <v-row>
        <v-col cols="6" align="start">
          <h2>Collections</h2>
        </v-col>
        <!-- <v-col cols="6" align="end">
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
        </v-col> -->
      </v-row>
      <v-row>
        <v-col cols="12" align="start">
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
        no-data-text="Aucune collection trouvée"
        no-results-text="Aucune collection trouvée"
        loading-text="Chargement en cours..."
        v-model="selectedCollections"
        :headers="headersCollections"
        :items="collections"
        :search="searchCollections"
        item-key="id"
        show-select
        class="elevation-1"
      ></v-data-table>
      <hr class="mt-8 mb-8" />
      <!-- /Collections -->
      <!-- Dossiers -->
      <v-row>
        <v-col cols="6" align="start">
          <h2>Dossiers</h2>
        </v-col>
        <!-- <v-col cols="6" align="end">
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
        </v-col> -->
      </v-row>
      <v-row>
        <v-col cols="12" align="start">
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
        no-data-text="Aucun dossier trouvé"
        no-results-text="Aucun dossier trouvé"
        loading-text="Chargement en cours..."
        v-model="selectedCollections"
        :headers="headersCollections"
        :items="collections"
        :search="searchCollections"
        item-key="id"
        show-select
        class="elevation-1"
      ></v-data-table>
      <hr class="mt-8 mb-8" />
      <!-- /Dossiers -->
      <!-- Analyses -->
      <v-row>
        <v-col cols="6" align="start">
          <h2>Analyses</h2>
        </v-col>
        <!-- <v-col cols="6" align="end">
          <v-btn small class="mx-2" color="primary">Ajouter une analyse</v-btn>
          <v-btn small color="error" :disabled="true"
            >Supprimer la sélection</v-btn
          >
        </v-col> -->
      </v-row>
      <v-row>
        <v-col cols="12" align="start">
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
      <hr class="mt-8 mb-8" />
      <!-- /Analyses -->
      <!-- Rapports -->
      <v-row>
        <v-col cols="6" align="start">
          <h2>Rapports</h2>
        </v-col>
        <!-- <v-col cols="6" align="end">
          <v-btn small class="mx-2" color="primary" @click="ajouterTextes"
            >Ajouter un rapport</v-btn
          >
          <v-btn small color="error" :disabled="true"
            >Supprimer la sélection</v-btn
          >
        </v-col> -->
      </v-row>
      <v-row>
        <v-col cols="12" align="start">
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
      <!-- /Rapports -->
    </v-container>
  </div>
</template>

<script>
// Importations
import axios from "axios";
import { TabsData } from "../../flux/Tabs";
import { DialogsData } from "../../flux/Dialogs";

// Exportation de la fonction
export default {
  props: {
    content: Object
  },
  data: () => ({
    snackbarAjoute: false,
    titre: "",
    paternite: "",
    linkAnalyse: "",
    link: "",
    // Ajout d'une analyse
    searchAnalyses: "",
    selectedAnalyses: [],
    headersAnalyses: [
      { text: "Titre", value: "titre" },
      { text: "Type d'analyse", value: "type" },
      { text: "Ressources de l'auteur", value: "ressources" }
    ],
    analyses: [],
    // Ajout d'un rapport
    searchRapports: "",
    selectedRapports: [],
    headersRapports: [
      { text: "Titre", value: "titre" },
      { text: "Type de rapport", value: "type" }
    ],
    rapports: [],
    // Ajout d'une version
    searchVersions: "",
    selectedVersions: [],
    headersVersions: [
      { text: "Titre", value: "titre" },
      { text: "# de mots", value: "nbmots" },
      { text: "Type de prétraitement", value: "typepretraitement" },
      { text: "Spécifications", value: "specification" },
      { text: "Commentaires", value: "commentaires" }
    ],
    versions: [],
    // Ajout d'une collection
    selectedCollections: [],
    searchCollections: "",
    headersCollections: [
      { text: "Titre", value: "titre" },
      { text: "# de textes par l'auteur", value: "nbtextes" },
      { text: "# de mots par l'auteur", value: "nbmots" }
    ],
    collections: [],
    dialogCollections: false,
    rechercheAjoutsCollections: "",
    selectedAjoutsCollections: [],
    contentCollections: [],
    // Ajout d'un dossier
    selectedDossiers: [],
    searchDossiers: "",
    headersDossiers: [
      { text: "Titre", value: "titre" },
      { text: "# de textes par l'auteur", value: "nbtextes" },
      { text: "# de mots par l'auteur", value: "nbmots" }
    ],
    dossiers: [],
    dialogDossiers: false,
    rechercheAjoutsDossiers: "",
    selectedAjoutsDossiers: [],
    contentDossiers: [],
    // Ajouter profil
    searchProfils: "",
    selectedProfils: [],
    headersProfils: [
      { text: "Type", value: "type" },
      { text: "Alias", value: "alias" },
      { text: "Prénom NOM", value: "nom" }
    ],
    headersProfilsT: [
      { text: "Type", value: "typeP" },
      { text: "Alias", value: "alias" },
      { text: "Prénom NOM", value: "nom" }
    ],
    profils: [],
    disabledProfils: true,
    dialogProfils: false,
    rechercheAjoutsProfils: "",
    selectedAjoutsProfils: [],
    contentProfils: [],
    loadingProfils: true
  }),
  methods: {
    majTexte() {
      // TypeProfils
      // Ajout en formulaire
      let formData = new FormData();
      formData.append("id", this.content.id);
      formData.append("type", "Texte");
      formData.append("get", "Profil");

      // Appel avec axios
      axios
        .post(process.env.VUE_APP_SERVEUR + "/assoc", formData)
        .then(response => {
          let result = JSON.parse(response.data);
          console.log("The result :");
          console.log(result);
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
        .catch(error => {
          console.log(error);
          this.loadingProfils = false;
        });
      // /TypeProfils
    },
    nouveauProfil() {
      DialogsData.open("profil-connu");
      DialogsData.addToFolder("Texte", this.content.id);
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
    associerProfils() {
      if (confirm("Voulez-vous vraiment ajouter cette association ?")) {
        let formData = new FormData();
        this.selectedAjoutsProfils.map(e => {
          formData = new FormData();
          formData.append("champs1", "Texte");
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
              newFormData.append("type", "Texte");
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
    fermerProfils() {
      DialogsData.init();
      this.majTexte();
      this.dialogProfils = false;
    },
    sauvegarder() {
      // Sauvegarder les modifications
      // Ajout en formulaire
      let formData = new FormData();
      formData.append("id", this.content.id);
      formData.append("alias", this.content.titre);
      formData.append("paternite", this.content.paternite);
      formData.append("specification", this.content.specification);
      formData.append("typeEcriture", this.content.typeEcriture);
      formData.append("segmentation", this.content.segmentation);
      formData.append("registre", this.content.registre);
      formData.append("commentaire", this.content.commentaire);

      // Appel avec axios
      axios
        .post(process.env.VUE_APP_SERVEUR + "/modifier-texte", formData)
        .then(response => {
          console.log(response);
          this.snackbarAjoute = true;
        })
        .catch(error => {
          console.log(error);
        });
    },
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
    },
    deleteProfils() {
      // Message de suppression de profil
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
              newFormData.append("type", "Texte");
              newFormData.append("get", "Profil");

              // Appel avec axios
              axios
                .post(process.env.VUE_APP_SERVEUR + "/assoc", newFormData)
                .then(response => {
                  let result = JSON.parse(response.data);
                  this.profils = result;
                  this.snackbarSupprimer = true;
                  this.majTexte();
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
    }
  },
  created() {
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
    this.majTexte();
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
  },
  updated: function() {
    // Profils
    if (this.selectedProfils.length > 0) {
      this.disabledProfils = false;
    } else {
      this.disabledProfils = true;
    }
    // Textes
  }
};
</script>

<style scoped>
.border-iframe {
  border: 1px black solid;
}
</style>
