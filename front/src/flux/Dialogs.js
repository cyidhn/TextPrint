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
		ngchars: false,
		racines: false,
		reinert: false,
		ngpos: false,
		lemmes: false,
		bagofwords: false,
		classification: false,
		stateInFolder: false,
		nameFolder: "",
		numberFolder: 0,
	},
	open(n) {
		if (n === "ngmots") {
			this.state.ngmots = true;
		}
		if (n === "reinert") {
			this.state.reinert = true;
		}
		if (n === "racines") {
			this.state.racines = true;
		}
		if (n === "bagofwords") {
			this.state.bagofwords = true;
		}
		if (n === "lemmes") {
			this.state.lemmes = true;
		}
		if (n === "classification") {
			this.state.classification = true;
		}
		if (n === "ngpos") {
			this.state.ngpos = true;
		}
		if (n === "ngchars") {
			this.state.ngchars = true;
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
		if (n === "reinert") {
			this.state.reinert = false;
		}
		if (n === "racines") {
			this.state.racines = false;
		}
		if (n === "lemmes") {
			this.state.lemmes = false;
		}
		if (n === "bagofwords") {
			this.state.bagofwords = false;
		}
		if (n === "classification") {
			this.state.classification = false;
		}
		if (n === "ngpos") {
			this.state.ngpos = false;
		}
		if (n === "ngchars") {
			this.state.ngchars = false;
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
