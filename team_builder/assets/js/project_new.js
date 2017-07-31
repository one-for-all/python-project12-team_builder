!(function (root) {
  exports = {}

  function gatherData () {
    const data = {
      'title': document.getElementById('title').value,
      'description': document.getElementById('description').value,
      'timeline': document.getElementById('timeline').value,
      'applicant_requirements': document.getElementById('applicant_requirements').value,
      'positions': []
    }
    const positions = document.getElementsByClassName('position')
    for (let i = 0; i < positions.length; i++) {
      const position = positions[i]
      data.positions.push({
        'title': position.getElementsByClassName('position_title')[0].value,
        'description': position.getElementsByClassName('position_description')[0].value,
        'skill': position.getElementsByClassName('position_skill')[0].value
      })
    }
    return data
  }

  function newProject (data) {
    const newProjectURL = 'api/v1/projects/'
    const xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function () {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status >= 200 && xhr.status <= 299) {
          const resp = JSON.parse(xhr.responseText)
          window.location.href = resp.project_url
        } else {
          const error = JSON.parse(xhr.responseText).error
          utilities.showBannerErrorMessage(error)
        }
      }
    }
    xhr.open('POST', newProjectURL)
    xhr.setRequestHeader('Content-Type', 'application/json')
    xhr.setRequestHeader('X-CSRFToken', Cookies.get('csrftoken'))
    xhr.send(JSON.stringify(data))
  }

  exports.formSubmit = function (event) {
    event.preventDefault()
    const data = gatherData()
    newProject(data)
  }

  document.getElementById('form').onsubmit = exports.formSubmit

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = exports
  } else {
    root.projectNewModule = exports
  }
}(this))
