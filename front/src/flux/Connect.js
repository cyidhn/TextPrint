// 
// Flux Connect
// @DemangeJeremy
// 

// Store Connect
export const ConnectData = {
    debug: true,
    state: {
        connect: false
    },
    connexion() {
        this.state.connect = true;
    },
    deconnexion() {
        this.state.connect = false;
    }
}