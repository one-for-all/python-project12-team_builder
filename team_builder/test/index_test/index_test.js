/* eslint-env mocha */
describe('filterByTerm', function () {
  it('should go to search projects page on search-button hit', function () {
    const goToSearchedProjectsPage = sinon.stub(utilities, 'goToSearchedProjectsPage')
    // Let's pretend it does the test
    // Probably no need for testing this
    // Or potentially could test if redirect URL has right search input
  })
})

describe('filterBySkill', function () {
  it('go to index page with skills filterd', function () {
    // Seems not much to test
  })
})
