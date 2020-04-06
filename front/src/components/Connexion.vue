<template>
  <v-container>
    <v-snackbar v-model="barinfo" :bottom="true" color="error" :timeout="3000">
      Le login ou le mot de passe sont incorrectes. Merci de réessayer.
      <v-btn dark text @click="snackbarSupprimer = false">Fermer</v-btn>
    </v-snackbar>
    <v-row>
      <v-col class="justify-center">
        <h1 class="blue--text text--darken-4 text-center">
          TEXT |
          <b>PRINT</b>
        </h1>
        <h4 class="mt-2 text-center">
          Connectez-vous pour accéder à l'application
        </h4>
        <v-form ref="form" class="mt-8">
          <v-text-field v-model="login" label="Login" required></v-text-field>
          <v-text-field
            type="password"
            v-model="mdp"
            label="Mot de passe"
            required
          ></v-text-field>
          <v-btn block color="primary" class="mt-4" @click="connexion"
            >Se connecter</v-btn
          >
        </v-form>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
// Importations
import { ConnectData } from "../flux/Connect";

// Exportations de la fonction
export default {
  data: () => ({
    login: "",
    mdp: "",
    connecte: "",
    barinfo: false,
  }),

  methods: {
    connexion() {
      if (
        (this.login === "idhn" && this.mdp === "idhn3") ||
        (this.login === "alexandra" && this.mdp === "idhn_chemiirita") ||
        (this.login === "julien" && this.mdp === "idhn2020!")
      ) {
        this.setCookie("ctex", "3", 1);
        ConnectData.connexion();
      } else {
        this.setCookie("ctex", "1", 1);
        this.barinfo = true;
      }
    },
    setCookie(cname, cvalue, exdays) {
      var d = new Date();
      d.setTime(d.getTime() + exdays * 24 * 60 * 60 * 1000);
      var expires = "expires=" + d.toUTCString();
      document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
    },
  },
};
</script>
