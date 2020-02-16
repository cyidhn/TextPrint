/// <reference types="Cypress" />

context('(Reconnexion suite à deconnexion - Problème Cypress)', () => {

    it('Reconnexion', () => {

      // Login vrai
      cy.get('#login')
        .clear()
        .type('idhn').should('have.value', 'idhn')

      cy.get('#password')
        .clear()
        .type('idhn3').should('have.value', 'idhn3')

      cy.get('#connexionButton').click()

    })
  
  })
  