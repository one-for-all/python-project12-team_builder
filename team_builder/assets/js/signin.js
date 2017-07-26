/*
  Signin button on click: POST entered info to signin API
    SUCCESS: redirect to home page
    ERROR: display error banner
*/
!(function (root) {
  exports = {}

  exports.signin = function (data) {
    const signinURL = '/accounts/api/v1/login/'
    const xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function () {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status <= 200 && xhr.status <= 299) {
          utilities.goToHomePage()
        } else {
          const error = JSON.parse(xhr.responseText).error
          utilities.showBannerErrorMessage(error)
        }
      }
    }
    xhr.open('POST', signinURL)
    xhr.setRequestHeader('Content-Type', 'application/json')
    xhr.setRequestHeader('X-CSRFToken', Cookies.get('csrftoken'))
    xhr.send(JSON.stringify(data))
  }

  exports.gatherData = function () {
    return {
      'email': document.getElementById('email').value,
      'password': document.getElementById('password').value
    }
  }

  exports.formSubmit = function (event) {
    event.preventDefault()
    const data = exports.gatherData()
    exports.signin(data)
  }

  const form = document.getElementById('form')
  form.onsubmit = exports.formSubmit

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = exports
  } else {
    root.signinModule = exports
  }
}(this))
