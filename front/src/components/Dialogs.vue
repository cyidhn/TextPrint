<template>
	<div>
		<CreateProfilConnu />
		<CreateProfilAnonyme />
		<CreateCollection />
		<CreateDossier />
		<CreateTexte />
		<NgramsMots />
	</div>
</template>

<script>
	import CreateProfilConnu from "./dialogs/CreateProfilConnu";
	import CreateProfilAnonyme from "./dialogs/CreateProfilAnonyme";
	import CreateCollection from "./dialogs/CreateCollection";
	import CreateDossier from "./dialogs/CreateDossier";
	import CreateTexte from "./dialogs/CreateTexte";
	import NgramsMots from "./dialogs/NgramsMots";

	export default {
		components: {
			CreateProfilConnu,
			CreateCollection,
			CreateDossier,
			CreateProfilAnonyme,
			CreateTexte,
			NgramsMots,
		},
	};
</script>
