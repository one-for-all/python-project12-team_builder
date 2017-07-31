!(function (root) {
  exports = {}

  exports.showBannerErrorMessage = function (error) {
    const body = document.getElementById('body')
    const topElement = document.getElementById('top')
    let errorBanner = document.getElementById('error-banner')
    if (!errorBanner) {
      errorBanner = document.createElement('div')
      errorBanner.id = 'error-banner'
    }
    errorBanner.innerHTML = '<h2>Error</h2>'
    for (let prop in error) {
      if (prop === 'non_field_errors') {
        errorBanner.innerHTML += `<p>${error[prop]}</p>`
      } else {
        errorBanner.innerHTML += `<p>${prop}: ${error[prop]}</p>`
      }
    }
    body.insertBefore(errorBanner, topElement)
  }

  exports.goToSearchedProjectsPage = function () {
    const searchTerm = document.getElementById('search-projects').value.trim()
    const destinationURL = encodeURI(`?term=${searchTerm}`)
    window.location.href = destinationURL
  }

  exports.goToSigninPage = function () {
    window.location.href = '/accounts/signin/'
  }

  exports.goToHomePage = function () {
    window.location.href = '/'
  }

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = exports
  } else {
    root.utilities = exports
  }
}(this))
