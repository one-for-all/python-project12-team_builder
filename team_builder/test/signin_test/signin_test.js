/* eslint-env mocha */
describe('formSubmit', function () {
  const emailInput = document.getElementById('email')
  const passwordInput = document.getElementById('password')
  let xhr
  let request
  before(function () {
    emailInput.value = 'test'
    passwordInput.value = 'password'
    xhr = sinon.useFakeXMLHttpRequest()
    xhr.onCreate = function (req) { request = req }
  })
  it('should post to signin API with stringified json data', function () {
    const event = document.createEvent('Event')
    signinModule.formSubmit(event)
    expect(request.url).to.equal('/accounts/api/v1/login/')
    expect(JSON.parse(request.requestBody)).to.eql({
      'email': 'test',
      'password': 'password'
    })
    expect(request.requestHeaders).include.all.keys('Content-Type', 'X-CSRFToken')
  })
  it('should call go to home page on success', function () {
    const stub = sinon.stub(utilities, 'goToHomePage')
    const event = document.createEvent('Event')
    signinModule.formSubmit(event)
    request.respond(200)
    assert(stub.calledOnce)
  })
  it('should call show banner error on error', function () {
    const stub = sinon.stub(utilities, 'showBannerErrorMessage')
    const event = document.createEvent('Event')
    signinModule.formSubmit(event)
    request.respond(400, '', '{ "error" : "" }')
    assert(stub.calledOnce)
  })
})
