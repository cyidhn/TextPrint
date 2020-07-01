<template>
	<div>
		<CreateProfilConnu />
		<CreateProfilAnonyme />
		<CreateCollection />
		<CreateDossier />
		<CreateTexte />
		<NgramsMots />
		<Classification />
		<Lemmes />
		<BagOfWords />
		<NgramsChars />
		<NgramsCatGram />
	</div>
</template>

<script>
	import CreateProfilConnu from "./dialogs/CreateProfilConnu";
	import CreateProfilAnonyme from "./dialogs/CreateProfilAnonyme";
	import CreateCollection from "./dialogs/CreateCollection";
	import CreateDossier from "./dialogs/CreateDossier";
	import CreateTexte from "./dialogs/CreateTexte";
	import NgramsMots from "./dialogs/NgramsMots";
	import NgramsChars from "./dialogs/NgramsChars";
	import NgramsCatGram from "./dialogs/NgramsCatGram";
	import Classification from "./dialogs/Classification";
	import Lemmes from "./dialogs/Lemmes";
	import BagOfWords from "./dialogs/BagOfWords";

	export default {
		components: {
			CreateProfilConnu,
			CreateCollection,
			CreateDossier,
			CreateProfilAnonyme,
			CreateTexte,
			NgramsMots,
			NgramsChars,
			NgramsCatGram,
			Classification,
			BagOfWords,
			Lemmes,
		},
	};
</script>
