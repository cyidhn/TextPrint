<template>
  <v-container>
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
export default {
  props: {
    login: String,
    mdp: String,
    connecte: Boolean,
    barinfo: Boolean
  },

  methods: {
    connexion() {
      if (
        (this.login === "idhn" && this.mdp === "idhn3") ||
        (this.login === "alexandra" && this.mdp === "idhn_chemiirita")
      ) {
        this.connecte = true;
      } else {
        this.barinfo = true;
      }
    }
  }
};
</script>