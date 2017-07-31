!(function (root) {
  exports = {}

  exports.filterBySkill = function (event) {
    event.preventDefault()
    const skill = event.target.textContent
    const destinationURL = encodeURI(`/?skill=${skill}`)
    window.location.href = destinationURL
  }

  const skillFilters = document.getElementsByClassName('skill-filter')
  for (let i = 0; i < skillFilters.length; i++) {
    skillFilters[i].onclick = exports.filterBySkill
  }

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = exports
  } else {
    root.indexModule = exports
  }
}(this))
