<template>
  <div>
    <!-- Champs recherche -->
    <div v-if="contentTabs.nowId === 1">
      <transition name="slide-fade">
        <div
          style="overflow: scroll; padding-bottom: 300px;"
          :key="id"
          class="taille-f"
        >
          <h1>{{ title }}</h1>
          <br />
          <Search />
        </div>
      </transition>
    </div>
    <!-- /Champs recherche -->

    <!-- Texte -->
    <div v-if="type === 'Texte'">
      <transition name="slide-fade">
        <div style="overflow: scroll;" :key="id" class="taille-f">
          <div class="my-2 float-right" v-if="contentTabs.nowId != 1">
            <v-btn
              @click="removeTab"
              v-shortkey="['ctrl', 'x']"
              @shortkey="removeTab()"
              depressed
              small
              color="error"
              >X Fermer la fenêtre</v-btn
            >
          </div>
          <br />
          <br />
          <br />
          <hr />
          <br />
          <h1>Texte : {{ title }}</h1>
          <br />
          <Texte :content="save" />
        </div>
      </transition>
    </div>
    <!-- /Texte -->

    <!-- Dossiers -->
    <div v-if="type === 'Dossiers'">
      <transition name="slide-fade">
        <div style="overflow: scroll;" :key="id" class="taille-f">
          <div class="my-2 float-right" v-if="contentTabs.nowId != 1">
            <v-btn
              @click="removeTab"
              v-shortkey="['ctrl', 'x']"
              @shortkey="removeTab()"
              depressed
              small
              color="error"
              >X Fermer la fenêtre</v-btn
            >
          </div>
          <br />
          <br />
          <br />
          <hr />
          <br />
          <Dossier :content="save" />
        </div>
      </transition>
    </div>
    <!-- /Dossiers -->

    <!-- Collections -->
    <div v-if="type === 'Collections'">
      <transition name="slide-fade">
        <div style="overflow: scroll;" :key="id" class="taille-f">
          <div class="my-2 float-right" v-if="contentTabs.nowId != 1">
            <v-btn
              @click="removeTab"
              v-shortkey="['ctrl', 'x']"
              @shortkey="removeTab()"
              depressed
              small
              color="error"
              >X Fermer la fenêtre</v-btn
            >
          </div>
          <br />
          <br />
          <br />
          <hr />
          <br />
          <Collection :content="save" />
        </div>
      </transition>
    </div>
    <!-- /Collections -->

    <!-- Profil -->
    <div v-if="type === 'Profil'">
      <transition name="slide-fade">
        <div style="overflow: scroll;" :key="id" class="taille-f">
          <div class="my-2 float-right" v-if="contentTabs.nowId != 1">
            <v-btn
              v-shortkey="['ctrl', 'x']"
              @shortkey="removeTab()"
              @click="removeTab"
              depressed
              small
              color="error"
              >X Fermer la fenêtre</v-btn
            >
          </div>
          <br />
          <br />
          <br />
          <hr />
          <br />
          <Profil :personne="title" :content="save" />
        </div>
      </transition>
    </div>
    <!-- /Profil -->
  </div>
</template>

<script>
// Importations
import { TabsData } from "../flux/Tabs";

// Exportation de la fonction
export default {
  components: {
    Search: () => import("./Search"),
    Texte: () => import("./windows/Texte"),
    Dossier: () => import("./windows/Dossier"),
    Collection: () => import("./windows/Collection"),
    Profil: () => import("./windows/Profil"),
  },
  props: {
    id: Number,
    content: Array,
  },

  data: () => ({
    title: "",
    type: "",
    save: [],
    contentTabs: TabsData.state,
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
    },
  },

  beforeUpdate() {
    this.fetchProps();
  },

  mounted() {
    this.fetchProps();
  },
};
</script>

<style scoped>
/* Les animations d'entrée (« enter ») et de sortie (« leave »)  */
/* peuvent utiliser différentes fonctions de durée et de temps.  */
.slide-fade-enter-active {
  transition: all 0.2s ease;
  transition-delay: 0.2s;
}
.slide-fade-leave-active {
  transition: all 0.2ws ease;
}
.slide-fade-enter, .slide-fade-leave-to
/* .slide-fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
.taille-f {
  height: 84.5vh;
}
</style>
