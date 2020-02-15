<template>
  <v-container>
    <ul>
      <li v-for="(eco) in ecosystem" :key="eco.id">
        <a :href="eco.href" target="_blank">{{eco.text}}</a>
        <button @click="supprimer(eco.id)">Supprimer</button>
      </li>
    </ul>
    <v-form>
      <v-text-field v-model="myText" label="Texte" required></v-text-field>

      <v-text-field v-model="myLink" label="Lien" required></v-text-field>

      <v-btn color="success" class="mr-4" @click="add">Ajouter à la liste</v-btn>
    </v-form>
  </v-container>
</template>

<script>
import { MenuData, Add_MenuData, Delete_MenuData } from "../flux/Menu";

export default {
  name: "Menu",
  data: () => ({
    ecosystem: MenuData,
    myText: "",
    myLink: ""
  }),
  methods: {
    add() {
      Add_MenuData(this.myText, this.myLink);
      this.myText = "";
      this.myLink = "";
    },
    supprimer(param) {
      Delete_MenuData(param);
    }
  }
};
</script>