<template>
  <transition name="slide-fade">
    <div v-if="contentTabs.nowId === 1">
      <div :key="id" class="taille-f">
        <h1>{{title}}</h1>
        <br />
        <Search />
      </div>
    </div>
    <div v-else>
      <div :key="id" class="taille-f">
        <div class="my-2 float-right" v-if="contentTabs.nowId != 1">
          <v-btn @click="removeTab" depressed small color="error">X Fermer la fenêtre</v-btn>
        </div>
        <h1>{{title}}</h1>
        <br />
        <p>Quam ob rem cave Catoni anteponas ne istum quidem ipsum, quem Apollo, ut ais, sapientissimum iudicavit; huius enim facta, illius dicta laudantur. De me autem, ut iam cum utroque vestrum loquar, sic habetote.</p>
        <p>Et olim licet otiosae sint tribus pacataeque centuriae et nulla suffragiorum certamina set Pompiliani redierit securitas temporis, per omnes tamen quotquot sunt partes terrarum, ut domina suscipitur et regina et ubique patrum reverenda cum auctoritate canities populique Romani nomen circumspectum et verecundum.</p>
        <p>Superatis Tauri montis verticibus qui ad solis ortum sublimius attolluntur, Cilicia spatiis porrigitur late distentis dives bonis omnibus terra, eiusque lateri dextro adnexa Isauria, pari sorte uberi palmite viget et frugibus minutis, quam mediam navigabile flumen Calycadnus interscindit.</p>
      </div>
    </div>
  </transition>
</template>

<script>
import { TabsData } from "../flux/Tabs";
import Search from "./Search";

export default {
  components: {
    Search
  },
  props: {
    id: Number,
    content: Array
  },

  data: () => ({
    title: "",
    contentTabs: TabsData.state
  }),

  methods: {
    fetchProps() {
      for (let i = 0; i < this.content.length; i++) {
        if (this.content[i].id === this.id) {
          console.log(this.content[i].title);
          this.title = this.content[i].title;
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
  height: 100vh;
}
</style>