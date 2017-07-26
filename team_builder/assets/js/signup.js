/*
  Signup button on click: POST entered info to signup API
    SUCCESS: redirect to signin page
    ERROR: display errorr message banner
*/
!(function (root) {
  const exports = {}

  exports.signup = function (data) {
    const signupURL = '/accounts/api/v1/signup/'
    const xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function () {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status >= 200 && xhr.status <= 299) {
          utilities.goToSigninPage()
        } else {
          const error = JSON.parse(xhr.responseText).error
          utilities.showBannerErrorMessage(error)
        }
      }
    }
    xhr.open('POST', signupURL)
    xhr.setRequestHeader('Content-Type', 'application/json')
    xhr.setRequestHeader('X-CSRFToken', Cookies.get('csrftoken'))
    xhr.send(JSON.stringify(data))
  }

  exports.gatherData = function () {
    return {
      username: document.getElementById('username').value,
      email: document.getElementById('email').value,
      password: document.getElementById('password').value,
      confirm_password: document.getElementById('confirm_password').value
    }
  }

  const form = document.getElementById('form')
  form.onsubmit = function (event) {
    event.preventDefault()
    const data = exports.gatherData()
    exports.signup(data)
  }

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = exports
  } else {
    root.signupModule = exports
  }
}(this))
