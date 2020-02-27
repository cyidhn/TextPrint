<template>
  <v-app>
    <v-container fluid>
      <!-- Snackbar -->
      <v-snackbar v-model="barinfo" :bottom="true" color="error" :timeout="3000">
        Le login ou le mot de passe est incorrect.
        <v-btn dark text @click="snackbarSupprimer = false">Fermer</v-btn>
      </v-snackbar>
      <!-- /Snackbar -->
      <div v-if="connecte">
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
        <Connexion :login="login" :mdp="mdp" :connecte="connecte" :barinfo="barinfo" />
      </div>
    </v-container>
  </v-app>
</template>

<script>
import Tabs from "./components/Tabs";
import Menu from "./components/Menu";
import Dialogs from "./components/Dialogs";
import Connexion from "./components/Connexion";
// import CreateProfil from "./components/dialogs/CreateProfilConnu";

export default {
  name: "App",

  components: {
    Tabs,
    Menu,
    Dialogs,
    Connexion
  },

  data: () => ({
    login: "",
    mdp: "",
    connecte: true,
    barinfo: false
  })
};
</script>

<style scoped>
body {
  max-height: 100vh;
  overflow: hidden;
}
</style>
