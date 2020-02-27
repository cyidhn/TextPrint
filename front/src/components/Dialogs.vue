<template>
  <div>
    <CreateProfilConnu />
    <CreateCollection />
    <CreateDossier />
  </div>
</template>

<script>
import CreateProfilConnu from "./dialogs/CreateProfilConnu";
import CreateCollection from "./dialogs/CreateCollection";
import CreateDossier from "./dialogs/CreateDossier";

export default {
  components: {
    CreateProfilConnu,
    CreateCollection,
    CreateDossier
  }
};
</script>
