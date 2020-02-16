// 
// Flux Menu
// @DemangeJeremy
// 

// Store MenuData
export let MenuData = {
    debug: true,
    state: {
        id: 4,
        data: [{
                id: 1,
                text: 'vuetify-loader',
                href: 'https://github.com/vuetifyjs/vuetify-loader',
            },
            {
                id: 2,
                text: 'github',
                href: 'https://github.com/vuetifyjs/vuetify',
            },
            {
                id: 3,
                text: 'awesome-vuetify',
                href: 'https://github.com/vuetifyjs/awesome-vuetify',
            },
        ]
    },
    add(text, href) {
        this.state.data = [...this.state.data, {
            id: this.state.id,
            text,
            href
        }];
        this.state.id = this.state.id + 1;
    },
    delete(id) {
        let newData = [...this.state.data];
        console.log(newData);
        for (let i = 0; i < this.state.data.length; i++) {
            if (this.state.data[i].id === id) {
                newData.splice(i, 1);
            }
        }
        this.state.data = newData;
    }
}