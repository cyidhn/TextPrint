<template>
  <v-card>
    <v-tabs v-model="contentTabs.tab" background-color="black lighten-2" dark>
      <v-tab
        v-for="n in contentTabs.data"
        :key="n.id"
        @click="callEvent(n.id)"
        >{{ n.title }}</v-tab
      >
    </v-tabs>
    <v-card-text class="text-center">
      <v-divider class="mx-4" vertical></v-divider>
      <Content :id="contentTabs.nowId" :content="contentTabs.data" />
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
