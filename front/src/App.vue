<template>
  <v-app>
    <v-content>
      <Tabs />
      <Menu />
    </v-content>
  </v-app>
</template>

<script>
import Menu from "./components/Menu";
import Tabs from "./components/Tabs";

export default {
  name: "App",

  components: {
    Menu,
    Tabs
  },

  data: () => ({
    //
  })
};
</script>
