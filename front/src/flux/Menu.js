// 
// Flux Menu
// @DemangeJeremy
// 

// Déclaration de variables
let Id_MenuData = 3;

// Variable de sauvegarde de données
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

// Méthode pour ajouter une données au tableau
export function Add_MenuData(text, href) {
    MenuData.push({id: ++Id_MenuData, text, href});
}

// Méthode pour supprimer un objet du tableau
export function Delete_MenuData(id) {
    for(let i = 0; i < MenuData.length; i++){ 
        if (MenuData[i].id === id) {
            MenuData.splice(i, 1); 
        }
     }
}