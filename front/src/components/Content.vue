<template>
  <div>
    <h1>Contenu de l'id {{id}} || {{title}}</h1>
    <br />
    <p>Quam ob rem cave Catoni anteponas ne istum quidem ipsum, quem Apollo, ut ais, sapientissimum iudicavit; huius enim facta, illius dicta laudantur. De me autem, ut iam cum utroque vestrum loquar, sic habetote.</p>
    <p>Et olim licet otiosae sint tribus pacataeque centuriae et nulla suffragiorum certamina set Pompiliani redierit securitas temporis, per omnes tamen quotquot sunt partes terrarum, ut domina suscipitur et regina et ubique patrum reverenda cum auctoritate canities populique Romani nomen circumspectum et verecundum.</p>
    <p>Superatis Tauri montis verticibus qui ad solis ortum sublimius attolluntur, Cilicia spatiis porrigitur late distentis dives bonis omnibus terra, eiusque lateri dextro adnexa Isauria, pari sorte uberi palmite viget et frugibus minutis, quam mediam navigabile flumen Calycadnus interscindit.</p>
  </div>
</template>

<script>
export default {
  props: {
    id: Number,
    content: Array
  },

  data: () => ({
    title: ""
  }),

  methods: {
    fetchProps() {
      for (let i = 0; i < this.content.length; i++) {
        if (this.content[i].id === this.id) {
          console.log(this.content[i].title);
          this.title = this.content[i].title;
        }
      }
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