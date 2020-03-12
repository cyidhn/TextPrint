<template>
  <v-app>
    <v-container fluid>
      <div v-if="etat.connect">
        <v-row no-gutters>
          <Dialogs />
          <v-col lg="2">
            <Menu />
          </v-col>
          <v-col lg="10">
            <Tabs />
          </v-col>
        </v-row>
      </div>
      <div v-else>
        <Connexion />
      </div>
    </v-container>
  </v-app>
</template>

<script>
import Tabs from "./components/Tabs";
import Menu from "./components/Menu";
import Dialogs from "./components/Dialogs";
import Connexion from "./components/Connexion";
import { ConnectData } from "./flux/Connect";
// import CreateProfil from "./components/dialogs/CreateProfilConnu";

export default {
  name: "App",

  components: {
    Tabs,
    Menu,
    Dialogs,
    Connexion
  },

  mounted: function() {
    console.log(`TextPrint - Version 1.02 | Laboratoire IDHN`);
  },

  data: () => ({
    etat: ConnectData.state
  })
};
</script>

<style scoped>
body {
  max-height: 100vh;
  overflow: hidden;
}
</style>
