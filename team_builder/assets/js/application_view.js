!(function (root) {
  exports = {}

  function getApplication (event) {
    const tr = event.target.parentNode.parentNode
    return tr.id
  }

  function constructXHR (event) {
    const applicationID = getApplication(event)
    const actionAPI = `/api/v1/application/${applicationID}/`
    const redirectURL = '/applications/'
    const xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function () {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status >= 200 && xhr.status <= 299) {
          window.location.href = redirectURL
        } else {
          const error = JSON.parse(xhr.responseText).error
          utilities.showBannerErrorMessage(error)
        }
      }
    }
    xhr.open('POST', actionAPI)
    xhr.setRequestHeader('Content-Type', 'application/json')
    xhr.setRequestHeader('X-CSRFToken', Cookies.get('csrftoken'))
    return xhr
  }

  exports.approveApplicant = function (event) {
    event.stopPropagation()
    const xhr = constructXHR(event)
    xhr.send(JSON.stringify({
      action: 'approve'
    }))
  }

  exports.rejectApplicant = function (event) {
    event.stopPropagation()
    const xhr = constructXHR(event)
    xhr.send(JSON.stringify({
      action: 'reject'
    }))
  }

  const approveButtons = document.getElementsByClassName('approve-button')
  for (let i = 0; i < approveButtons.length; i++) {
    approveButtons[i].onclick = exports.approveApplicant
  }

  const rejectButtons = document.getElementsByClassName('reject-button')
  for (let i = 0; i < rejectButtons.length; i++) {
    rejectButtons[i].onclick = exports.rejectApplicant
  }

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = exports
  } else {
    root.applicationModule = exports
  }
}(this))
