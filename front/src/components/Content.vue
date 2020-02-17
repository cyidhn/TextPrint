<template>
  <transition name="slide-fade">
    <div v-if="contentTabs.nowId === 1">
      <div
        style="overflow: scroll; padding-bottom:300px"
        :key="id"
        class="taille-f"
      >
        <h1>{{ title }}</h1>
        <br />
        <Search />
      </div>
    </div>
    <div v-if="type === 'Texte'">
      <div style="overflow: scroll" :key="id" class="taille-f">
        <div class="my-2 float-right" v-if="contentTabs.nowId != 1">
          <v-btn @click="removeTab" depressed small color="error"
            >X Fermer la fenêtre</v-btn
          >
        </div>
        <h1>{{ title }}</h1>
        <br />
        <Texte :content="save" />
      </div>
    </div>
  </transition>
</template>

<script>
import { TabsData } from "../flux/Tabs";
import Search from "./Search";
import Texte from "./windows/Texte";

export default {
  components: {
    Search,
    Texte
  },
  props: {
    id: Number,
    content: Array
  },

  data: () => ({
    title: "",
    type: "",
    save: [],
    contentTabs: TabsData.state
  }),

  methods: {
    fetchProps() {
      for (let i = 0; i < this.content.length; i++) {
        if (this.content[i].id === this.id) {
          this.title = this.content[i].title;
          this.type = this.content[i].contains[0].type;
          this.save = this.content[i].contains[0];
        }
      }
    },

    removeTab() {
      TabsData.remove(TabsData.state.nowId);
    }
  },

  beforeUpdate() {
    this.fetchProps();
  },

  mounted() {
    this.fetchProps();
  }
};
</script>

<style>
/* Les animations d'entrée (« enter ») et de sortie (« leave »)  */
/* peuvent utiliser différentes fonctions de durée et de temps.  */
.slide-fade-enter-active {
  transition: all 0.3s ease;
  transition-delay: 0.3s;
}
.slide-fade-leave-active {
  transition: all 0.3s ease;
}
.slide-fade-enter, .slide-fade-leave-to
/* .slide-fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}

.taille-f {
  height: 84.5vh;
}
</style>
