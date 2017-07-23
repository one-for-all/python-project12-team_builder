$('#form').submit(function(evt) {
  evt.preventDefault();
  const data = $(this).serializeArray();
  let data_obj = {};
  /* Raw Input Assembling */
  for (let i = 0; i < data.length; i++) {
    data_obj[data[i].name] = data[i].value;
  }
  /* Manage position input */
  delete data_obj.position_description;
  delete data_obj.position_title;
  delete data_obj.skills;
  data_obj.positions = [];
  $('.position-existing').each(function(index, li) {
    data_obj.positions.push({
      title: $(li).children('[name="position_title"]').val(),
      description: $(li).children('[name="position_description"]').val(),
      skill: $(li).children('[name="skills"]').val(),
      exists: true
    });
  });
  $('.position-new').each(function(index, $li) {
    data_obj.positions.push({
      title: $(li).children('[name="position_title"]').val(),
      description: $(li).children('[name="position_description"]').val(),
      skill: $(li).children('[name="skills"]').val(),
      exists: false
    });
  });
  console.log(data_obj);
  const url = $(this).attr('action');
  $.post(url, JSON.stringify(data_obj), () => {
    alert('success');
  }, 'json');
});
