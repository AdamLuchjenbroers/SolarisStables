function update_action_info() {
  id = $('#id_action option:selected').val();

  if (id == "") {
    $('#preview-action-name').text('Action Effects')
    $('#preview-action').html('')
    $('#id_cost').val(0)
    
    $('#stable-action-submit').attr('disabled','yes');

    return;
  }

  $.ajax({
    type : 'get'
  , url  : '/reference/actions/' + id + '/json'
  , dataType: 'json'
  }).done(function(response) {
    $('#preview-action-name').text(response['action'])
    $('#preview-action').html(response['description'])
    $('#id_cost').val(response['base_cost'])

    $('#stable-action-submit').removeAttr('disabled');
  });
}

$( document ).ready(function() {
  $('#id_action').change(update_action_info);
});
