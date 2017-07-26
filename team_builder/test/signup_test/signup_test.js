/* eslint-env mocha */
describe('gatherData', function () {
  const usernameInput = document.getElementById('username')
  const emailInput = document.getElementById('email')
  const passwordInput = document.getElementById('password')
  const confirmPasswordInput = document.getElementById('confirm_password')
  before(function () {
    usernameInput.value = 'test'
    emailInput.value = 'test@example.com'
    passwordInput.value = 'password'
    confirmPasswordInput.value = 'password'
  })

  it('Should correctly assemble data from inputs and return as an object', function () {
    const data = signupModule.gatherData()
    expect(data).to.eql({
      'username': 'test',
      'email': 'test@example.com',
      'password': 'password',
      'confirm_password': 'password'
    })
  })
})

describe('signup', function () {
  let xhr
  let data
  let request

  before(function () {
    data = {
      'username': 'test',
      'email': 'test@example.com',
      'password': 'password',
      'confirm_password': 'password'
    }
    xhr = sinon.useFakeXMLHttpRequest()
    xhr.onCreate = function (req) { request = req }
  })

  it('should POST to signup API url with stringified data', function () {
    signupModule.signup(data)
    expect(request.url).to.equal('/accounts/api/v1/signup/')
    expect(request.method).to.equal('POST')
    expect(JSON.parse(request.requestBody)).to.eql(data)
    expect(request.requestHeaders).include.all.keys('Content-Type', 'X-CSRFToken')
  })

  it('should go to sign in page on success', function () {
    var stub = sinon.stub(utilities, 'goToSigninPage')
    signupModule.signup(data)
    request.respond(200)
    assert(stub.calledOnce)
  })

  it('should show error message in banner on failure', function () {
    var stub = sinon.stub(utilities, 'showBannerErrorMessage')
    signupModule.signup(data)
    const error = {
      'email': 'already registered'
    }
    request.respond(400, {'Content-Type': 'application/json'}, `{"error": ${JSON.stringify(error)}}`)
    assert(stub.withArgs(error).calledOnce)
  })
})
