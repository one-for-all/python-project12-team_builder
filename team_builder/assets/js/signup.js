function signup(data) {
  const xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function () {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (200 <= xhr.status && xhr.status <= 299) {
        
      } else {

      }
    }
  };
  const url = '/accounts/api/v1/signup/';
  xhr.open('POST', url);
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.send(JSON.stringify(data));
}

function gatherData() {
  let data = {
    username: document.getElementById('username').value,
    email: document.getElementById('email').value,
    password: document.getElementById('password').value,
    confirm_password: document.getElementById('confirm_password').value
  };
  return data;
}

const form = document.getElementById('form');
form.onsubmit = function (event) {
  event.preventDefault();
  const data = gatherData();
  signup(data);
};

// $('#form').submit(function(evt) {
//   evt.preventDefault();
//   //const url = window.location.origin + '/accounts/api/v1/signup/';
//   const url = '/accounts/api/v1/signup/';
//   data = $('#form').serializeArray();
//   obj = {};
//   for (let i = 0; i < data.length; i++) {
//     obj[data[i].name] = data[i].value;
//   }
//   $.post(url, obj, function(response) {
//     alert(response);
//   }).fail(function(xhr, status, error) {
//     console.log(xhr);
//     console.log(status);
//     console.log(error);
//   });
// });
