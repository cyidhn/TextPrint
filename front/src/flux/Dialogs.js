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
		texte: false,
		ngmots: false,
		stateInFolder: false,
		nameFolder: "",
		numberFolder: 0,
	},
	open(n) {
		if (n === "ngmots") {
			this.state.ngmots = true;
		}
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
	addToFolder(name, number) {
		this.state.stateInFolder = true;
		this.state.nameFolder = name;
		this.state.numberFolder = number;
	},
	init() {
		this.state.stateInFolder = false;
	},
	close(n) {
		if (n === "ngmots") {
			this.state.ngmots = false;
		}
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
	},
};
