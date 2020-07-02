<template>
	<v-row justify="center">
		<!-- Modal ajouter un texte -->
		<v-dialog v-model="dialogTextes" max-width="500px" persistent scrollable>
			<v-card>
				<v-card-title>
					<span class="headline">
						<b>Ajouter un texte</b>
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
					<v-btn color="blue darken-1" text @click="addTexte">Ajouter</v-btn>
				</v-card-actions>
			</v-card>
		</v-dialog>
		<!-- /Modal ajouter un texte -->
		<v-dialog v-model="data.reinert" persistent scrollable max-width="500px">
			<v-card>
				<v-card-title>Reinert</v-card-title>
				<v-divider></v-divider>
				<v-card-text style="height: 200px;">
					<v-form ref="form" v-model="valid" lazy-validation>
						<v-row>
							<v-col cols="12">
								<div v-if="!selectedAjoutsTextes.length">
									<p>
										Avant de créer une version, vous devez sélectionner un
										texte.
									</p>
									<v-btn small color="primary" @click="ajouterTextes"
										>Sélectionner un texte</v-btn
									>
								</div>
								<div v-else>
									<p>
										Texte sélectionné :
										<b>{{ selectedAjoutsTextes[0].titre }}</b>
									</p>
									<v-btn small color="primary" @click="ajouterTextes"
										>Modifier le texte sélectionné</v-btn
									>
									<h4 class="mt-2" v-if="loadingBtn">
										Votre demande est en cours de traitement. Merci de patienter
										quelques instants.
									</h4>
								</div>
							</v-col>
						</v-row>
					</v-form>
				</v-card-text>
				<v-divider></v-divider>
				<v-card-actions>
					<v-btn
						v-shortkey="['ctrl', 'x']"
						@shortkey="checkDialog"
						color="blue darken-1"
						text
						@click="checkDialog"
						>Fermer</v-btn
					>
					<v-btn
						color="blue darken-1"
						:disabled="!selectedAjoutsTextes.length || loadingBtn"
						text
						@click="validate"
						>Générer le résultat</v-btn
					>
				</v-card-actions>
			</v-card>
		</v-dialog>
	</v-row>
</template>

<script>
	// Importations
	import { DialogsData } from "../../flux/Dialogs";
	import axios from "axios";

	// Exportation de la fonction
	export default {
		name: "CreateDossier",
		data: () => ({
			// Chargement
			loadingBtn: false,
			// Ajouts textes
			dialogTextes: false,
			rechercheAjoutsTextes: "",
			selectedAjoutsTextes: [],
			contentTextes: [],
			loadingTextes: true,
			headersTextes: [
				{ text: "Titre", value: "titre" },
				{ text: "# Versions", value: "version" },
				{ text: "Voir", value: "actions", sortable: false },
			],
			// Autre
			data: DialogsData.state,
			dialogm1: "",
			dialog: false,
			valid: true,
			nom: "",
			nomRules: [
				(v) => !!v || "Le nombre de N est requis.",
				(v) =>
					/^(([2-9])|([1][0-9])|20)$/.test(v) ||
					"Le nombre doit être compris entre 2 et 20.",
			],
		}),
		computed: {
			filteredListTextes() {
				return this.contentTextes.filter((p) => {
					return p.titre
						.toLowerCase()
						.includes(this.rechercheAjoutsTextes.toLowerCase());
				});
			},
		},
		methods: {
			addTexte() {
				console.log("Ajout d'un texte");
				this.dialogTextes = false;
				console.log(this.selectedAjoutsTextes[0]);
			},
			ajouterTextes() {
				this.selectedAjoutsTextes = [];
				let formData = new FormData();
				formData.append("req", "");
				axios
					.post(process.env.VUE_APP_SERVEUR + "/searchtextes", formData)
					.then((response) => {
						this.contentTextes = response.data;
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
			checkDialog() {
				DialogsData.close("reinert");
			},
			reset() {
				this.$refs.form.reset();
			},
			validate() {
				if (this.$refs.form.validate()) {
					// Ajout en formulaire
					let formData = new FormData();
					formData.append("id", this.selectedAjoutsTextes[0].id);
					formData.append("fichier", this.selectedAjoutsTextes[0].fichier);
					this.loadingBtn = true;

					// Appel avec axios
					axios
						.post(process.env.VUE_APP_SERVEUR + "/traitement-reinert", formData)
						.then((response) => {
							// begin
							// Appel avec axios
							console.log(response.data);
							alert("L'analyse a bien été ajoutée dans le texte.");
							DialogsData.close("reinert");
							this.loadingBtn = false;
						})
						.catch((error) => {
							alert(error.response.data);
							this.loadingBtn = false;
						});
				} else {
					alert(
						"Merci de vérifier que les champs soient correctement complétés."
					);
				}
			},
			resetValidation() {
				this.$refs.form.resetValidation();
			},
		},
	};
</script>
