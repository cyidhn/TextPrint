// 
// Flux Dialogs
// @DemangeJeremy
// 

// Store DialogsData
export const DialogsData = {
    debug: true,
    state: {
        profilConnu: false,
        profilAnonyme: false,
        collection: false,
        dossier: false,
        texte: false
    },
    open(n) {
        if (n === "profil-connu") {
            this.state.profilConnu = true;
        }
        if (n === "texte") {
            this.state.texte = true;
        }
        if (n === "profil-anonyme") {
            this.state.profilAnonyme = true;
        }
        if (n === "collection") {
            this.state.collection = true;
        }
        if (n === "dossier") {
            this.state.dossier = true;
        }
    },
    close(n) {
        if (n === "profil-connu") {
            this.state.profilConnu = false;
        }
        if (n === "profil-anonyme") {
            this.state.profilAnonyme = false;
        }
        if (n === "collection") {
            this.state.collection = false;
        }
        if (n === "dossier") {
            this.state.dossier = false;
        }
        if (n === "texte") {
            this.state.texte = false;
        }
    }
}