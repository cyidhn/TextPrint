export let MenuData = [
    {
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
];

let Id_MenuData = 3;


export function Add_MenuData(text, href) {
    MenuData.push({id: ++Id_MenuData, text, href});
}