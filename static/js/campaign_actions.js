function submit_start_week() {
  button = $(this);

  $.ajax({
    type : 'post'
  , url  : button.attr('action_url')
  , dataType : 'json'
  , data : { 'start_week' : button.attr('start_week') }
  }).success(function(response) {
    button.attr('start_week', response['next_state']);
    button.text(response['button_text']);

    refresh_section('#campaign-stables-part', no_handler);
  });
}

$( document ).ready(function() {
  $('#campaign-action-start').click(submit_start_week);
});
