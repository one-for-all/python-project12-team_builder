/* eslint-env mocha */
describe('filterBySkill', function () {
  let xhr
  let request
  before(function () {
    xhr = sinon.useFakeXMLHttpRequest()
    xhr.onCreate = function (req) { request = req }
  })
  it('should send data to search project API')
  it('should display results on page on success')
  it('should display error banner on error')
})
