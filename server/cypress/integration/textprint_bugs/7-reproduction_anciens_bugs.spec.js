/// <reference types="Cypress" />

context('Reproduction des anciens bugs', () => {

    it('Recherche d\'un profil connu spécifique', () => {
        
  
        cy.get('#recherche')
          .type('Paul ', { delay: 100 })
        
        cy.get('button.list-group-item') 
          .click({ force: true })
  
        cy.get('.ui-tabs-anchor') 
          .contains('Paul Durand')
          .click({ force: true })
  
        cy.get('button.supprimer-button-texte') 
          .click({ force: true })
  
        cy.on('window:confirm', (str) => {
          expect(str).contains(`Voulez-vous vraiment supprimer ce profil définitivement ?`)
        })
          
      })
  
  })