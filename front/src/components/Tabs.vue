<template>
  <v-card>
    <v-tabs v-model="contentTabs.tab" background-color="blue darken-4" dark>
      <v-tab
        v-for="n in contentTabs.data"
        :key="n.id"
        @click="callEvent(n.id)"
        >{{ n.affichage }}</v-tab
      >
    </v-tabs>
    <v-card-text class="text-center">
      <v-divider class="mx-4" vertical></v-divider>
      <Content :id="contentTabs.nowId" :content="contentTabs.data" />
    </v-card-text>
  </v-card>
</template>

<script>
import { TabsData } from "../flux/Tabs";

export default {
  data: () => ({
    contentTabs: TabsData.state,
    textTitle: "",
    length: 2,
  }),

  components: {
    Content: () => import("./Content"),
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
    },
  },
};
</script>
