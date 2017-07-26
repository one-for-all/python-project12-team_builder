/* eslint-env mocha */
describe('apply', function () {
  let xhr
  let request
  before(function () {
    xhr = sinon.useFakeXMLHttpRequest()
    xhr.onCreate = function (req) { request = req }
  })
  it('should send data to apply project API')
  it('should redirect to project page on success')
  it('should display error banner on error')
})
