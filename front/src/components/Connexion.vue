<template>
  <v-container>
    <v-snackbar v-model="barinfo" :bottom="true" color="error" :timeout="3000">
      Le login ou le mot de passe sont incorrectes. Merci de réessayer.
      <v-btn dark text @click="snackbarSupprimer = false">Fermer</v-btn>
    </v-snackbar>
    <v-col class="justify-center">
      <h1>TextPrint V.1.02</h1>
      <v-form ref="form">
        <v-text-field v-model="login" label="Login" required></v-text-field>
        <v-text-field type="password" v-model="mdp" label="Mot de passe" required></v-text-field>
        <v-btn color="success" class="mr-4" @click="connexion">Se connecter</v-btn>
      </v-form>
    </v-col>
  </v-container>
</template>

<script>
import { ConnectData } from "../flux/Connect";

export default {
  data: () => ({
    login: "",
    mdp: "",
    connecte: "",
    barinfo: false
  }),

  methods: {
    connexion() {
      if (
        (this.login === "idhn" && this.mdp === "idhn3") ||
        (this.login === "alexandra" && this.mdp === "idhn_chemiirita")
      ) {
        ConnectData.connexion();
      } else {
        this.barinfo = true;
      }
    }
  }
};
</script>