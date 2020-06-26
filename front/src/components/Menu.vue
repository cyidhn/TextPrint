<template>
	<v-card height="97vh">
		<v-navigation-drawer absolute permanent left width="100%">
			<template v-slot:prepend>
				<v-list-item two-line>
					<h1 class="blue--text text--darken-4">
						TEXT |
						<b>PRINT</b>
					</h1>
				</v-list-item>
			</template>
			<div v-shortkey="['ctrl', 't']" @shortkey="eventClick('texte')"></div>
			<div
				v-shortkey="['ctrl', 'alt', 't']"
				@shortkey="eventClick('texte')"
			></div>
			<div
				v-shortkey="['ctrl', 'alt', 'c']"
				@shortkey="eventClick('profil-connu')"
			></div>
			<div
				v-shortkey="['ctrl', 'alt', 'a']"
				@shortkey="eventClick('profil-anonyme')"
			></div>
			<div
				v-shortkey="['ctrl', 'alt', 'd']"
				@shortkey="eventClick('dossier')"
			></div>
			<div
				v-shortkey="['ctrl', 'alt', 'o']"
				@shortkey="eventClick('collection')"
			></div>
			<div
				v-shortkey="['ctrl', 'c']"
				@shortkey="eventClick('profil-connu')"
			></div>
			<div
				v-shortkey="['ctrl', 'a']"
				@shortkey="eventClick('profil-anonyme')"
			></div>
			<div v-shortkey="['ctrl', 'd']" @shortkey="eventClick('dossier')"></div>
			<div
				v-shortkey="['ctrl', 'o']"
				@shortkey="eventClick('collection')"
			></div>
			<v-divider></v-divider>

			<v-list dense>
				<v-list-item
					v-for="item in items"
					:key="item.title"
					@click="eventClick(item.link)"
				>
					<v-list-item-icon>
						<v-icon>{{ item.icon }}</v-icon>
					</v-list-item-icon>
					<v-list-item-content>
						<v-list-item-title v-html="item.title"></v-list-item-title>
					</v-list-item-content>
				</v-list-item>
			</v-list>
		</v-navigation-drawer>
	</v-card>
</template>

<script>
	import { TabsData } from "../flux/Tabs";
	import { DialogsData } from "../flux/Dialogs";
	import { ConnectData } from "../flux/Connect";

	export default {
		data: () => ({
			principal: [
				{ title: "Bases de données", icon: "mdi-database", link: "database" },
				{
					title: "Importer un fichier",
					icon: "mdi-file",
					link: "texte",
				},
				{ title: "Nouveau", icon: "mdi-pencil", link: "nouveau" },
				{ title: "Versions", icon: "mdi-timelapse", link: "versions" },
				{ title: "Analyses", icon: "mdi-file-find", link: "analyses" },
				{ title: "Rapports", icon: "mdi-folder-lock", link: "rapports" },
				{ title: "Paramètres", icon: "mdi-message-alert", link: "params" },
			],
			analyses: [
				{
					title: "<b>Retour</b>",
					icon: "mdi-keyboard-backspace",
					link: "retour",
				},
				{ title: "Classification", icon: "mdi-file", link: "classification" },
			],
			versions: [
				{
					title: "<b>Retour</b>",
					icon: "mdi-keyboard-backspace",
					link: "retour",
				},
				{ title: "// Racines", icon: "mdi-file", link: "rien" },
				{ title: "// Lemmes", icon: "mdi-file", link: "rien" },
				{ title: "Étiquettes grammaticales", icon: "mdi-file", link: "egram" },
				{ title: "N-grammes", icon: "mdi-file", link: "ngrammes" },
			],
			egram: [
				{
					title: "<b>Retour</b>",
					icon: "mdi-keyboard-backspace",
					link: "versions",
				},
				{ title: "Catégories grammaticales", icon: "mdi-file", link: "rien" },
				{
					title: "Mots outils vs Mots lexicaux",
					icon: "mdi-file",
					link: "rien",
				},
			],
			ngrammes: [
				{
					title: "<b>Retour</b>",
					icon: "mdi-keyboard-backspace",
					link: "versions",
				},
				{ title: "N-grammes de caractères", icon: "mdi-file", link: "ngchars" },
				{ title: "N-grammes de mots", icon: "mdi-file", link: "ngmots" },
				{
					title: "N-grammes de catégories grammaticales",
					icon: "mdi-file",
					link: "ngpos",
				},
				{ title: "// N-grammes de racines", icon: "mdi-file", link: "rien" },
				{ title: "// N-grammes de lemmes", icon: "mdi-file", link: "rien" },
			],
			fichier: [
				{
					title: "<b>Retour</b>",
					icon: "mdi-keyboard-backspace",
					link: "retour",
				},
				{ title: "Ouvrir", icon: "mdi-file", link: "ouvrir" },
				{ title: "Importer", icon: "mdi-pencil", link: "importer" },
			],
			params: [
				{
					title: "<b>Retour</b>",
					icon: "mdi-keyboard-backspace",
					link: "retour",
				},
				{ title: "Déconnexion", icon: "mdi-run", link: "deconnexion" },
			],
			nouveau: [
				{
					title: "<b>Retour</b>",
					icon: "mdi-keyboard-backspace",
					link: "retour",
				},
				{
					title: "Profil connu",
					icon: "mdi-account-outline",
					link: "profil-connu",
				},
				{
					title: "Profil anonyme",
					icon: "mdi-account",
					link: "profil-anonyme",
				},
				{ title: "Texte", icon: "mdi-file", link: "texte" },
				{ title: "Dossier", icon: "mdi-folder", link: "dossier" },
				{
					title: "Collection",
					icon: "mdi-folder-multiple",
					link: "collection",
				},
			],
			items: [],
		}),
		mounted: function() {
			this.items = [...this.principal];
		},
		methods: {
			back() {
				this.principal = true;
			},
			setCookie(cname, cvalue, exdays) {
				var d = new Date();
				d.setTime(d.getTime() + exdays * 24 * 60 * 60 * 1000);
				var expires = "expires=" + d.toUTCString();
				document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
			},
			eventClick(ref) {
				if (ref === "retour") {
					this.items = this.principal;
				}
				if (ref === "analyses") {
					this.items = this.analyses;
				}
				if (ref === "egram") {
					this.items = this.egram;
				}
				if (ref === "ngrammes") {
					this.items = this.ngrammes;
				}
				if (ref === "versions") {
					this.items = this.versions;
				}
				if (ref === "fichier") {
					this.items = this.fichier;
				}
				if (ref === "nouveau") {
					this.items = this.nouveau;
				}
				if (ref === "params") {
					this.items = this.params;
				}
				if (ref === "database") {
					TabsData.bdd();
				}
				if (ref === "ngmots") {
					DialogsData.open("ngmots");
				}
				if (ref === "classification") {
					DialogsData.open("classification");
				}
				if (ref === "ngpos") {
					DialogsData.open("ngpos");
				}
				if (ref === "ngchars") {
					DialogsData.open("ngchars");
				}
				if (ref === "profil-connu") {
					DialogsData.open("profil-connu");
				}
				if (ref === "profil-anonyme") {
					DialogsData.open("profil-anonyme");
				}
				if (ref === "collection") {
					DialogsData.open("collection");
				}
				if (ref === "dossier") {
					DialogsData.open("dossier");
				}
				if (ref === "texte") {
					DialogsData.open("texte");
				}
				if (ref === "deconnexion") {
					this.setCookie("ctex", "1", 1);
					ConnectData.deconnexion();
				}
			},
		},
	};
</script>
