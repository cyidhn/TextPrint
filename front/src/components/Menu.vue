<template>
    <v-container>
        <ul>
            <li v-for="(eco, i) in ecosystem" :key="i">
                <a :href="eco.href" target="_blank"> {{eco.text}}</a>
            </li>
        </ul>
    <v-form>
    <v-text-field
      v-model="myText"
      label="Texte"
      required
    ></v-text-field>

    <v-text-field
      v-model="myLink"
      label="Lien"
      required
    ></v-text-field>


    <v-btn
      color="success"
      class="mr-4"
      @click="add"
    >
      Valider
    </v-btn>
  </v-form>
    </v-container>
</template>

<script>
  import { MenuData, Add_MenuData } from "../flux/Menu";

  export default {

    name: 'Menu',
    data: () => ({
        ecosystem: MenuData,
        myText: '',
        myLink: '',
    }),
    methods: {
      add() {
        Add_MenuData(this.myText, this.myLink);
        this.myText = '';
        this.myLink = '';
      }
    },

  }
</script>