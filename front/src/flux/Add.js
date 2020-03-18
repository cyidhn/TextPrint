//
// Flux Add
// @DemangeJeremy
//

// Store Connect
export const AddData = {
  debug: true,
  state: {
    openWindow: false
  },
  open() {
    this.state.openWindow = true;
  },
  close() {
    this.state.openWindow = false;
  }
};
