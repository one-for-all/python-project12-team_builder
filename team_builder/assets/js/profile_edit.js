!(function (root) {
  exports = {}

  function updateProfile (data) {
    const updateProfileURL = '/accounts/api/v1/profile/'
    const redirectURL = '/accounts/profile/'
    const xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function () {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status <= 200 && xhr.status <= 299) {
          window.location.href = redirectURL
        } else {
          const error = JSON.parse(xhr.responseText).error
          utilities.appendErrorMessage(error)
        }
      }
    }
    xhr.open('POST', updateProfileURL)
    xhr.setRequestHeader('Content-Type', 'application/json')
    xhr.setRequestHeader('X-CSRFToken', Cookies.get('csrftoken'))
    xhr.send(JSON.stringify(data))
  }

  function gatherData () {
    const data = {
      'name': document.getElementById('name').value,
      'bio': document.getElementById('bio').value,
      'skills': []
    }
    const skills = document.getElementsByClassName('skills')
    for (let i = 0; i < skills.length; i++) {
      data.skills.push(skills[i].value)
    }
    return data
  }

  exports.formSubmit = function (event) {
    event.preventDefault()
    const data = gatherData()
    updateProfile(data)
  }

  const form = document.getElementById('form')
  form.onsubmit = exports.formSubmit

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = exports
  } else {
    root.profileEditModule = exports
  }
}(this))

// $('#form').submit(function(evt) {
//   evt.preventDefault();
//   const data = $(this).serializeArray();
//   let data_obj = {};
//   /* Raw Input Assembling */
//   for (let i = 0; i < data.length; i++) {
//     data_obj[data[i].name] = data[i].value;
//   }
//   /* Manage position input */
//   delete data_obj.position_description;
//   delete data_obj.position_title;
//   delete data_obj.skills;
//   data_obj.positions = [];
//   $('.position-existing').each(function(index, li) {
//     data_obj.positions.push({
//       title: $(li).children('[name="position_title"]').val(),
//       description: $(li).children('[name="position_description"]').val(),
//       skill: $(li).children('[name="skills"]').val(),
//       exists: true
//     });
//   });
//   $('.position-new').each(function(index, $li) {
//     data_obj.positions.push({
//       title: $(li).children('[name="position_title"]').val(),
//       description: $(li).children('[name="position_description"]').val(),
//       skill: $(li).children('[name="skills"]').val(),
//       exists: false
//     });
//   });
//   console.log(data_obj);
//   const url = $(this).attr('action');
//   $.post(url, JSON.stringify(data_obj), () => {
//     alert('success');
//   }, 'json');
// });
