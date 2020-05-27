<template>
	<div>
		<CreateProfilConnu />
		<CreateProfilAnonyme />
		<CreateCollection />
		<CreateDossier />
		<CreateTexte />
		<NgramsMots />
		<NgramsChars />
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

	export default {
		components: {
			CreateProfilConnu,
			CreateCollection,
			CreateDossier,
			CreateProfilAnonyme,
			CreateTexte,
			NgramsMots,
			NgramsChars,
		},
	};
</script>
