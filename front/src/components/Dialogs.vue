<template>
  <div>
    <CreateProfilConnu />
    <CreateProfilAnonyme />
    <CreateCollection />
    <CreateDossier />
  </div>
</template>

<script>
import CreateProfilConnu from "./dialogs/CreateProfilConnu";
import CreateProfilAnonyme from "./dialogs/CreateProfilAnonyme";
import CreateCollection from "./dialogs/CreateCollection";
import CreateDossier from "./dialogs/CreateDossier";

export default {
  components: {
    CreateProfilConnu,
    CreateCollection,
    CreateDossier,
    CreateProfilAnonyme
  }
};
</script>
