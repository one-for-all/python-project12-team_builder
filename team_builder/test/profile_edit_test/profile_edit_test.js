/* eslint-env mocha */
describe('formSubmit', function () {
  let xhr
  let request
  before(function () {
    xhr = sinon.useFakeXMLHttpRequest()
    xhr.onCreate = function (req) { request = req }
  })
  it('should send data to profile update API', function () {
    const event = document.createEvent('Event')
    profileEditModule.formSubmit(event)
    expect(request.url).to.equal('/accounts/api/v1/profile/')
    expect(request.requestHeaders).to.include.all.keys('X-CSRFToken', 'Content-Type')
  })
  it('should redirect to profile page on success')
  it('should display error banner on error')
})
