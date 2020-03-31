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
            >Changer à profil anonyme</v-btn
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
            >Changer à profil connu</v-btn
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
      <!-- Ajout un element -->
      <v-row class="mt-12">
        <v-col cols="6" align="start">
          <h2>Association avec les Textes</h2>
        </v-col>
        <!-- <v-col cols="6" align="end">
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
        </v-col> -->
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
      ></v-data-table>
      <br />
      <br />
      <br />
      <!-- /Ajout un element -->
      <!-- Ajout un element -->
      <v-row>
        <v-col cols="6" align="start">
          <h2>Association avec les Collections</h2>
        </v-col>
        <!-- <v-col cols="6" align="end">
          <v-btn small class="mx-2" color="primary" @click="ajouterCollections"
            >Ajouter une collection</v-btn
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
        <!-- <v-col cols="6" align="end">
          <v-btn small class="mx-2" color="primary" @click="ajouterTextes"
            >Ajouter une analyse</v-btn
          >
          <v-btn small color="error" :disabled="true"
            >Supprimer la sélection</v-btn
          >
        </v-col> -->
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

// Exportation de la fonction
export default {
  props: {
    content: Object,
    personne: String
  },

  data: () => ({
    // Gestion formulaire
    formulaire: [],
    identification: "",
    // Autre
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
    headersTextes: [
      { text: "Titre", value: "titre" },
      { text: "# Versions", value: "version" },
      { text: "Type de document", value: "typedoc" },
      { text: "Type d'écriture", value: "ecriture" },
      { text: "Segmentation", value: "segmentation" },
      { text: "Langue", value: "langue" },
      { text: "Thèmes", value: "themes" },
      { text: "Registre", value: "registre" },
      { text: "Audience", value: "audience" }
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
    headersGlobal: [
      { text: "Type", value: "type" },
      { text: "Titre", value: "titre" },
      { text: "Alias", value: "alias" },
      { text: "Prénom", value: "prenom" },
      { text: "Nom", value: "nom" }
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
    loadingCollections: true
  }),

  methods: {
    majProfil() {
      // Variable
      let formData = new FormData();

      // TypeTextes
      // Ajout en formulaire
      formData = new FormData();
      formData.append("id", this.content.id);
      formData.append("type", "Texte");
      formData.append("get", "Profil");

      // Appel avec axios
      axios
        .post(process.env.VUE_APP_SERVEUR + "/assoc", formData)
        .then(response => {
          let result = JSON.parse(response.data);
          this.textes = result;
          console.log("Textes :");
          console.log(this.textes);
          this.loadingTextes = false;
        })
        .catch(error => {
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
        .then(response => {
          let result = JSON.parse(response.data);
          this.collections = result;
          this.loadingCollections = false;
        })
        .catch(error => {
          console.log(error);
          this.loadingCollections = false;
        });
      // /TypeCollection
    },
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
          if (
            this.formulaire.alias == "" ||
            this.formulaire.alias == undefined
          ) {
            TabsData.changeName(
              TabsData.state.nowId,
              this.formulaire.prenom + " " + this.formulaire.nom
            );
            this.identification =
              this.formulaire.prenom + " " + this.formulaire.nom;
          } else {
            TabsData.changeName(TabsData.state.nowId, this.formulaire.alias);
            this.identification = this.formulaire.alias;
          }
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
    this.majProfil();
  }
};
</script>
