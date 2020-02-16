/// <reference types="Cypress" />

context('Connexion', () => {

    it('Saisie d\'un mauvais login et mot de passe', () => {

      cy.visit('http://127.0.0.1:5000/deconnexion')

      // Login faux
      cy.get('#login')
        .type('idhn', { delay: 100 }).should('have.value', 'idhn')

      cy.get('#password')
        .type('idhn', { delay: 100 }).should('have.value', 'idhn')

      cy.get('#connexionButton').click()

      cy.get('#alert-message')
        .should('not.have.class', 'd-none')

    })

    it('Saisie d\'un login et mot de passe correct', () => {

      // Login vrai
      cy.get('#login')
        .clear()
        .type('idhn', { delay: 100 }).should('have.value', 'idhn')

      cy.get('#password')
        .clear()
        .type('idhn3', { delay: 100 }).should('have.value', 'idhn3')

      cy.get('#connexionButton').click()

      cy.wait(3000)
      cy.url().should('eq', 'http://127.0.0.1:5000/page')
    })
  
  })
  