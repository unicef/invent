/// <reference types="Cypress" />
// https://on.cypress.io/interacting-with-elements

context('Edit project form', () => {
  it('is accessable from route: xy');
  it('isnt accessable as non logged in user');
  it('can be filled, has data');
  it('runs front-end validations before submitting');
  it('handles & shows back-end validations after submitting');
  it('can be saved as draft');
  it('as draft - isnt shown to non-eligible users');
  it('as draft - isnt editable by non-eligible users');
  it('as draft - is editable / saveable by eligible users');
  it('as draft - can be published by eligible users');
  it('as published - isnt shown to non-eligible users');
  it('as published - isnt editable by non-eligible users');
});
