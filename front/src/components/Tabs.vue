<template>
  <v-card>
    <v-tabs v-model="contentTabs.tab" background-color="black lighten-2" dark>
      <v-tab v-for="n in contentTabs.data" :key="n.id" @click="callEvent(n.id)">{{ n.title }}</v-tab>
    </v-tabs>
    <v-card-text class="text-center">
      <v-divider class="mx-4" vertical></v-divider>
      <div class="my-2 float-right" v-if="contentTabs.nowId != 1">
        <v-btn @click="removeTab" depressed small color="error">X Fermer la fenêtre</v-btn>
      </div>
      <Content :id="contentTabs.nowId" :content="contentTabs.data" />
      <v-text-field v-model="textTitle" label="Texte" required></v-text-field>
      <v-btn text @click="addTab">Ajouter Tab</v-btn>
    </v-card-text>
  </v-card>
</template>

<script>
import Content from "./Content";
import { TabsData } from "../flux/Tabs";

export default {
  data: () => ({
    contentTabs: TabsData.state,
    textTitle: "",
    length: 2
  }),

  components: {
    Content
  },

  methods: {
    addTab() {
      TabsData.add(this.textTitle);
      TabsData.change(this.contentTabs.id - 1);
      this.textTitle = "";
    },

    removeTab() {
      TabsData.remove(TabsData.state.nowId);
    },

    callEvent(id) {
      TabsData.change(id);
    }
  }
};
</script>