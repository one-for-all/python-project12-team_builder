/* eslint-env mocha */
describe('filter', function () {
  let xhr
  let request
  before(function () {
    xhr = sinon.useFakeXMLHttpRequest()
    xhr.onCreate = function (req) { request = req }
  })
  it('should send data to search application API')
  it('should display results on page on success')
  it('should display error banner on error')
})

describe('changeStatus', function () {
  let xhr
  let request
  before(function () {
    xhr = sinon.useFakeXMLHttpRequest()
    xhr.onCreate = function (req) { request = req }
  })
  it('should send data to change application status API')
  it('should display updates on page on success')
  it('should display error banner on error')
})
