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

  created: function() {
    let result = this.getCookie("ctex");
    if (result == "3") {
      ConnectData.connexion();
    }
  },

  methods: {
    setCookie(cname, cvalue, exdays) {
      var d = new Date();
      d.setTime(d.getTime() + exdays * 24 * 60 * 60 * 1000);
      var expires = "expires=" + d.toUTCString();
      document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
    },
    getCookie(cname) {
      var name = cname + "=";
      var decodedCookie = decodeURIComponent(document.cookie);
      var ca = decodedCookie.split(";");
      for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == " ") {
          c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
          return c.substring(name.length, c.length);
        }
      }
      return "";
    }
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
