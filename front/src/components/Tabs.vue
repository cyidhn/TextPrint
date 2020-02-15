<template>
  <v-card>
    <v-tabs
      v-model="tab"
      background-color="black lighten-2"
      dark
    >
      <v-tab
        v-for="n in contentTabs"
        :key="n.id"
      >
        {{ n.title }}
        <button @click="removeTab(n.id)">__X</button>
      </v-tab>
    </v-tabs>
    <v-card-text class="text-center">
    <v-divider class="mx-4" vertical></v-divider>
        <v-text-field
      v-model="textTitle"
      label="Texte"
      required
    ></v-text-field>
      <v-btn text @click="addTab">Ajouter Tab</v-btn>
    </v-card-text>
  </v-card>
</template>

<script>
  export default {
    data: () => ({
      contentTabs: [{id: 1, title: "A. Freeman"}],
      textTitle: '',
      id: 2,
      length: 2,
      tab: null,
    }),

    methods: {
      addTab() {
        this.contentTabs = [...this.contentTabs, {id: this.id, title: this.textTitle}];
        this.textTitle = "";
        this.id++;
      },

      removeTab(id) {
        for(let i = 0; i < this.contentTabs.length; i++){ 
            if (this.contentTabs[i].id === id) {
                this.contentTabs.splice(i, 1); 
            }
        }
      },
    },
  }
</script>