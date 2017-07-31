/* eslint-env mocha */
describe('bannerErrorMessage', function () {
  let error

  before(function () {
    error = {
      email: 'already registered'
    }
  })

  it('should present error on page', function () {
    utilities.showBannerErrorMessage(error)
    expect(document.body.innerHTML).to.have.string('already registered')
  })
})

