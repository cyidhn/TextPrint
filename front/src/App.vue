<template>
  <v-app>
    <v-container fluid>
      <v-row no-gutters>
        <v-col lg="2">
          <Menu />
        </v-col>
        <v-col lg="10">
          <Tabs />
        </v-col>
      </v-row>
    </v-container>
  </v-app>
</template>

<script>
import Tabs from "./components/Tabs";
import Menu from "./components/Menu";
// import CreateProfil from "./components/dialogs/CreateProfilConnu";

export default {
  name: "App",

  components: {
    Tabs,
    Menu
  },

  data: () => ({
    //
  })
};
</script>

<style>
body {
  max-height: 100vh;
  overflow: hidden;
}
</style>
