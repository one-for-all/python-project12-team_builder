!(function (root) {
  exports = {}

  function getPositionID (event) {
    return event.target.parentNode.id
  }

  exports.applyPosition = function (event) {
    const positionID = getPositionID(event)
    const applicationAPI = '/api/v1/applications/'
    const xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function () {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status >= 200 && xhr.status <= 299) {
          window.location.reload()
        } else {
          const error = JSON.parse(xhr.responseText).error
          utilities.showBannerErrorMessage(error)
        }
      }
    }
    xhr.open('POST', applicationAPI)
    xhr.setRequestHeader('Content-Type', 'application/json')
    xhr.setRequestHeader('X-CSRFToken', Cookies.get('csrftoken'))
    xhr.send(JSON.stringify({
      'position_id': positionID
    }))
  }

  const applyButtons = document.getElementsByClassName('apply-button')
  for (let i = 0; i < applyButtons.length; i++) {
    applyButtons[i].onclick = exports.applyPosition
  }

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = exports
  } else {
    root.projectViewModule = exports
  }
}(this))
