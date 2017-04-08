function update_action_info() {
  id = $('#id_action option:selected').val();

  $.ajax({
    type : 'get'
  , url  : '/reference/actions/' + id + '/json'
  , dataType: 'json'
  }).done(function(response) {
    $('#preview-action-name').text(response['action'])
    $('#preview-action').html(response['description'])
    $('#id_cost').val(response['base_cost'])
  });
}

$( document ).ready(function() {
  $('#id_action').change(update_action_info);
});
