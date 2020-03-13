//
// Flux Tabs
// @DemangeJeremy
//

// Store TabsData
export const TabsData = {
  debug: true,
  state: {
    tab: 0,
    tabTotal: 0,
    id: 2,
    nowId: 1,
    data: [
      {
        id: 1,
        title: "Base de données",
        affichage: "Base de données",
        contains: [
          {
            type: "search"
          }
        ]
      }
    ]
  },
  add(title, item) {
    this.state.data = [
      ...this.state.data,
      {
        id: this.state.id,
        affichage: title,
        title,
        contains: [item]
      }
    ];
    this.state.nowId = this.state.id;
    this.state.tab = this.state.tabTotal + 1;
    this.state.tabTotal = this.state.tabTotal + 1;
    this.state.id = this.state.id + 1;
  },
  change(id) {
    this.state.nowId = id;
    console.log("newId", id);
  },
  remove(id) {
    for (let i = 0; i < this.state.data.length; i++) {
      if (this.state.data[i].id === id) {
        this.state.data.splice(i, 1);
      }
    }
    this.state.tab = 0;
    this.state.nowId = 1;
    this.state.tabTotal = this.state.tabTotal - 1;
  },
  bdd() {
    this.state.tab = 0;
    this.state.nowId = 1;
  }
};
