// 
// Flux Dialogs
// @DemangeJeremy
// 

// Store DialogsData
export const DialogsData = {
    debug: true,
    state: {
        profilConnu: false
    },
    open(n) {
        if (n === "profil-connu") {
            this.state.profilConnu = true;
        }
    },
    close(n) {
        if (n === "profil-connu") {
            this.state.profilConnu = false;
        }
    }
}