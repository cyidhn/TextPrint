<template>
  <v-row justify="center">
    <v-dialog v-model="data.texte" persistent scrollable max-width="500px">
      <v-card>
        <v-card-title>Importer un texte</v-card-title>
        <v-divider></v-divider>
        <v-card-text style="height: 300px;">
          <v-form ref="form" v-model="valid" lazy-validation>
            <v-row>
              <v-col cols="12">
                <h2>Importation</h2>
              </v-col>
              <v-col cols="12">
                <input
                  accept=".txt"
                  type="file"
                  id="documentTexte"
                  ref="file"
                  @change="handleFileUpload()"
                />
                <p v-if="loadingText">
                  Le fichier est en cours d'analyse. Cela peut prendre plusieurs
                  minutes...
                </p>
                <p v-if="errorText">
                  <b
                    >Le fichier est non conforme, il doit être encodé en
                    UTF-8.</b
                  >
                  Merci de sélectionner un autre texte.
                </p>
              </v-col>
            </v-row>
            <v-row v-if="nextStep">
              <v-col cols="12" class="mt-8">
                <h2>Informations</h2>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  v-model="nom"
                  label="Titre du texte*"
                  autocomplete="nope"
                  hint="Donner un titre unique à votre nouveau texte."
                  :rules="nomRules"
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
                  v-model="typeDoc1"
                  :rules="typeDocRules"
                  label="Type de document*"
                  @change="handleChangeType1()"
                  required
                ></v-select>
                <v-select
                  v-if="viewTypeDoc2"
                  :items="getTypeDoc2"
                  v-model="typeDoc2"
                  @change="handleChangeType2()"
                  required
                ></v-select>
                <v-text-field
                  v-if="viewTypeDocAutre"
                  v-model="typeDocAutre"
                  label="Saisir le type du document"
                  autocomplete="nope"
                  required
                ></v-text-field>
                <v-text-field
                  v-model="specification"
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
                  v-model="typeEcriture"
                  label="Type d'écriture"
                  required
                ></v-select>
                <v-select
                  :items="[
                    'Non spécifiée',
                    'D\'origine',
                    'Passage',
                    'Compilation'
                  ]"
                  v-model="segmentation"
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
                  v-model="langue"
                  label="Langue (automatique)"
                  @change="changeLangue"
                  required
                ></v-select>
                <v-select
                  :items="['Non spécifié', 'Courant', 'Familier', 'Soutenu']"
                  v-model="registre"
                  label="Registre"
                  required
                ></v-select>
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
          <v-btn color="blue darken-1" text @click="checkDialog">Fermer</v-btn>
          <v-btn
            color="blue darken-1"
            v-if="!nextStep"
            :disabled="checkProgress"
            text
            @click="validate"
            >Importer le texte</v-btn
          >
          <v-btn
            color="blue darken-1"
            v-if="nextStep"
            text
            @click="validateNext"
            >Enregistrer le texte</v-btn
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
import axios from "axios";

// Exportation de la fonction
export default {
  name: "CreateTexte",
  data: () => ({
    // State
    data: DialogsData.state,
    // Emplacement du fichier
    file: "",
    // Gestion des erreurs du texte
    checkProgress: false,
    errorText: false,
    loadingText: false,
    nextStep: false,
    disabledImport: false,
    dialogm1: "",
    dialog: false,
    valid: true,
    // Identifiant
    nomFichier: "",
    // Titre
    nom: "",
    nomRules: [v => !!v || "Le titre est requis."],
    // Paternité
    paternite: "Non spécifié",
    paterniteRules: [v => !!v || "Le type de paternité est requis."],
    // Type de document
    typeDoc1: "",
    getTypeDoc2: [],
    viewTypeDoc2: false,
    typeDoc2: "",
    viewTypeDocAutre: false,
    typeDocAutre: "",
    typeDocRules: [v => !!v || "Le type de document requis."],
    // Spécification
    specification: "",
    // Type d'écriture
    typeEcriture: "Non spécifié",
    // Segmentation
    segmentation: "Non spécifiée",
    // Langue
    langue: "Non spécifiée",
    langueO: "",
    // Registre
    registre: "Non spécifié",
    // Commentaire
    commentaire: ""
  }),
  methods: {
    addWindow() {
      // Ajout en formulaire
      let formData = new FormData();

      // Appel avec axios
      axios
        .get(process.env.VUE_APP_SERVEUR + "/lastid-texte")
        .then(response => {
          formData.append("req", response.data[0].id);
          console.log(response.data[0].id);
          axios
            .post(process.env.VUE_APP_SERVEUR + "/search-texte", formData)
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
    changeLangue() {
      if (this.langueO != this.langue) {
        if (confirm("Êtes-vous sûr de vouloir changer la langue ?")) {
          this.langueO = this.langue;
          console.log(`Ici c'est ${this.langue}`);
        } else {
          this.langueOriginal();
        }
      }
    },
    langueOriginal() {
      this.langue = this.langueO;
    },
    checkDialog() {
      this.reset();
      DialogsData.close("texte");
    },
    reset() {
      this.$refs.form.reset();
      document.getElementById("documentTexte").value = "";
      this.$refs.form.resetValidation();
      this.sexe = "Non spécifié";
      this.education = "Non spécifié";
      this.sociale = "Non spécifiée";
      this.disabledImport = false;
      this.nextStep = false;
      this.viewTypeDoc2 = false;
      this.viewTypeDoc3 = false;
      this.viewTypeDocAutre = false;
    },
    handleChangeType1() {
      // Non spécifié
      if (this.typeDoc1 === "Non spécifié") {
        // Masquer les éléments
        this.viewTypeDoc2 = false;
        this.viewTypeDoc3 = false;
        this.viewTypeDocAutre = false;
      }

      // Autre
      if (this.typeDoc1 === "Autre") {
        // Masquer les éléments
        this.viewTypeDoc2 = false;
        this.viewTypeDoc3 = false;

        // Afficher le champs autre
        this.viewTypeDocAutre = true;
      }

      // Écriture personnelle
      if (this.typeDoc1 === "Écriture personnelle") {
        // Afficher les éléments
        this.viewTypeDoc2 = true;
        this.viewTypeDoc3 = false;
        this.viewTypeDocAutre = false;

        // Enregistre élément dans le select
        this.getTypeDoc2 = [
          "Jounal / Entrée d'un journal",
          "Notes personnelles",
          "Autre"
        ];
        this.typeDoc2 = this.getTypeDoc2[0];
      }

      // Correspondance
      if (this.typeDoc1 === "Correspondance") {
        // Afficher les éléments
        this.viewTypeDoc2 = true;
        this.viewTypeDoc3 = false;
        this.viewTypeDocAutre = false;

        // Enregistre élément dans le select
        this.getTypeDoc2 = [
          "Note",
          "Carte postale",
          "Lettre",
          "Email",
          "Autre"
        ];
        this.typeDoc2 = this.getTypeDoc2[0];
      }

      // Messagerie
      if (this.typeDoc1 === "Messagerie") {
        // Afficher les éléments
        this.viewTypeDoc2 = true;
        this.viewTypeDoc3 = false;
        this.viewTypeDocAutre = false;

        // Enregistre élément dans le select
        this.getTypeDoc2 = ["SMS", "Messagerie instantanée", "Autre"];
        this.typeDoc2 = this.getTypeDoc2[0];
      }

      // Web et réseaux sociaux
      if (this.typeDoc1 === "Web et réseaux sociaux") {
        // Afficher les éléments
        this.viewTypeDoc2 = true;
        this.viewTypeDoc3 = false;
        this.viewTypeDocAutre = false;

        // Enregistre élément dans le select
        this.getTypeDoc2 = [
          "Tweet",
          "Publication sur forum",
          "Publication sur Facebook",
          "Billet de blog",
          "Commentaires et interactions",
          "Autre"
        ];
        this.typeDoc2 = this.getTypeDoc2[0];
      }

      // Presse
      if (this.typeDoc1 === "Presse") {
        // Afficher les éléments
        this.viewTypeDoc2 = true;
        this.viewTypeDoc3 = false;
        this.viewTypeDocAutre = false;

        // Enregistre élément dans le select
        this.getTypeDoc2 = ["Article", "Journal", "Revue", "Autre"];
        this.typeDoc2 = this.getTypeDoc2[0];
      }

      // Rédactions Scientifiques et Académiques
      if (this.typeDoc1 === "Rédactions Scientifiques et Académiques") {
        // Afficher les éléments
        this.viewTypeDoc2 = true;
        this.viewTypeDoc3 = false;
        this.viewTypeDocAutre = false;

        // Enregistre élément dans le select
        this.getTypeDoc2 = [
          "Article",
          "Essai",
          "Dissertation",
          "Mémoire",
          "Rapport",
          "Revue scientifique",
          "Livre d'instruction",
          "Autre"
        ];
        this.typeDoc2 = this.getTypeDoc2[0];
      }

      // Rédactions littéraires
      if (this.typeDoc1 === "Rédactions littéraires") {
        // Afficher les éléments
        this.viewTypeDoc2 = true;
        this.viewTypeDoc3 = false;
        this.viewTypeDocAutre = false;

        // Enregistre élément dans le select
        this.getTypeDoc2 = [
          "Poésie",
          "Roman",
          "Pièce de théâtre",
          "Conte",
          "Fable",
          "Autobiographie ou mémoire",
          "Biographie",
          "Autre"
        ];
        this.typeDoc2 = this.getTypeDoc2[0];
      }

      // Rédactions judiciaires
      if (this.typeDoc1 === "Rédactions judiciaires") {
        // Afficher les éléments
        this.viewTypeDoc2 = true;
        this.viewTypeDoc3 = false;
        this.viewTypeDocAutre = false;

        // Enregistre élément dans le select
        this.getTypeDoc2 = ["Rapport", "Témoignage", "Lettre d'aveu", "Autre"];
        this.typeDoc2 = this.getTypeDoc2[0];
      }

      // Documents à intérêts judiciaires
      if (this.typeDoc1 === "Documents à intérêts judiciaires") {
        // Afficher les éléments
        this.viewTypeDoc2 = true;
        this.viewTypeDoc3 = false;
        this.viewTypeDocAutre = false;

        // Enregistre élément dans le select
        this.getTypeDoc2 = [
          "Lettre d'adieu",
          "Lettre de menace",
          "Demande de rançon",
          "Testament",
          "Autre"
        ];
        this.typeDoc2 = this.getTypeDoc2[0];
      }
    },
    handleChangeType2() {
      if (this.typeDoc2 === "Autre") {
        this.viewTypeDocAutre = true;
      } else {
        this.viewTypeDocAutre = false;
      }
    },
    handleFileUpload() {
      this.file = this.$refs.file.files[0];
    },
    validate() {
      if (this.$refs.form.validate()) {
        let formData = new FormData();
        formData.append("importer-texte", this.file);
        this.loadingText = true;
        this.disabledImport = true;
        this.errorText = false;
        // Verifier l'upload
        // Appel avec axios
        axios
          .post(process.env.VUE_APP_SERVEUR + "/verifier-texte", formData, {
            headers: {
              "Content-Type": "multipart/form-data"
            }
          })
          .then(response => {
            console.log(response);
            this.checkProgress = true;
            axios
              .post(process.env.VUE_APP_SERVEUR + "/importer-texte", formData, {
                headers: {
                  "Content-Type": "multipart/form-data"
                }
              })
              .then(response2 => {
                // Ajour des informations
                this.langue = response2.data.langue;
                this.langueO = response2.data.langue;
                this.nomFichier = response2.data.name;
                this.nom = this.file.name;
                this.loadingText = false;
                this.errorText = false;
                this.nextStep = true;
                this.checkProgress = false;
                //DialogsData.close("profil-connu");
              })
              .catch(error => {
                console.log(error);
                this.loadingText = false;
                this.errorText = true;
                this.disabledImport = false;
                this.checkProgress = false;
              });
            //DialogsData.close("profil-connu");
          })
          .catch(error => {
            console.log(error);
            this.loadingText = false;
            this.errorText = true;
            this.disabledImport = false;
            this.checkProgress = false;
          });
      }
    },
    validateNext() {
      console.log(this.paternite);
      if (this.paternite == "Non spécifié") {
        alert("Le champs type de paternité doit obligatoirement être rempli.");
      } else {
        if (this.$refs.form.validate()) {
          // Ajout en formulaire
          let formData = new FormData();
          formData.append("fichier", this.nomFichier);
          formData.append("titre", this.nom);
          formData.append("paternite", this.paternite);
          formData.append("typeDocument1", this.typeDoc1);
          formData.append("typeDocument2", this.typeDoc2);
          formData.append("typeDocument3", this.typeDocAutre);
          formData.append("specification", this.specification);
          formData.append("typeEcriture", this.typeEcriture);
          formData.append("segmentation", this.segmentation);
          formData.append("langue", this.langue);
          formData.append("registre", this.registre);
          formData.append("commentaire", this.commentaire);

          // Appel avec axios
          axios
            .post(process.env.VUE_APP_SERVEUR + "/importer-texte-bdd", formData)
            .then(response => {
              // begin
              // Appel avec axios
              axios
                .get(process.env.VUE_APP_SERVEUR + "/lastid-texte")
                .then(response => {
                  let idTexte = response.data[0].id;
                  console.log(idTexte);
                  // Si le folder est activé
                  if (DialogsData.state.stateInFolder == true) {
                    console.log("ok");
                    formData = new FormData();
                    formData.append("champs1", DialogsData.state.nameFolder);
                    formData.append("champs2", "Texte");
                    formData.append(
                      "idchamps1",
                      DialogsData.state.numberFolder
                    );
                    formData.append("idchamps2", idTexte);
                    // Appel avec axios
                    axios
                      .post(
                        process.env.VUE_APP_SERVEUR + "/associer-generalement",
                        formData
                      )
                      .then(response => {
                        if (
                          confirm(
                            "Le texte a bien été crée et ajouté. Souhaitez-vous l'ouvrir dans une autre fenêtre ?"
                          )
                        ) {
                          this.addWindow();
                        }
                        console.log(response.data);
                      })
                      .catch(error => {
                        console.error(error);
                      });
                  } else {
                    if (
                      confirm(
                        "Le texte a bien été crée. Souhaitez-vous l'ouvrir dans une autre fenêtre ?"
                      )
                    ) {
                      this.addWindow();
                    }
                  }
                })
                .catch(error => {
                  alert(error.response.data);
                });
              // /end
              console.log(response);
              this.reset();
              DialogsData.close("texte");
            })
            .catch(error => {
              console.log(error);
            });
        }
      }
    },
    resetValidation() {
      this.$refs.form.resetValidation();
      this.sexe = "Non spécifié";
      this.education = "Non spécifié";
      this.sociale = "Non spécifiée";
      this.disabledImport = false;
    }
  }
};
</script>
